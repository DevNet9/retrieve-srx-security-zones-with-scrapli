import asyncio
import xmltodict

from scrapli_netconf.driver import AsyncNetconfDriver
from scrapli.logging import enable_basic_logging
from jinja2 import Environment, FileSystemLoader

# Enable logging. Create a log file in the current directory.
enable_basic_logging(file=True, level="debug")

# setup jinja2 parameters
env = Environment(loader=FileSystemLoader('templates'),trim_blocks=True)
template = env.get_template('test.j2')

GALVESTON = {
    "host": "192.168.105.137",
    "auth_username": "scrapli",
    "auth_password": "juniper123",
    "auth_strict_key": False,
    "transport": "asyncssh"
}

SANANTONIO = {
    "host": "192.168.105.146",
    "auth_username": "scrapli",
    "auth_password": "juniper123",
    "auth_strict_key": False,
    "transport": "asyncssh"
}

DEVICES = [GALVESTON, SANANTONIO]

RPC = """
<get-zones-information>
</get-zones-information>
"""


async def gather_version(device):
    """Simple function to open a connection and get some data"""
    conn = AsyncNetconfDriver(**device)
    await conn.open()
    result = await conn.rpc(filter_=RPC)
    await conn.close()
    return result


async def main():
    """Function to gather coroutines, await them and print results"""
    coroutines = [gather_version(device) for device in DEVICES]
    results = await asyncio.gather(*coroutines)
    for each in results:
        reply_as_dict = xmltodict.parse(each.result)
        security_zones = reply_as_dict["rpc-reply"]["zones-information"]["zones-security"]

        output_from_parsed_template = template.render(security_zones=security_zones)
        print(output_from_parsed_template)

        # to save the results
        with open(f"{each.host}.yaml", "w") as fh:
            fh.write(output_from_parsed_template)

        # print(f"{each.host}")
        # for zone in security_zones:
        #     print(f'{zone["zones-security-zonename"]}')

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())