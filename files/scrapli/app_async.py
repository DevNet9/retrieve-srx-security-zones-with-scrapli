import asyncio

from scrapli_netconf.driver import AsyncNetconfDriver

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
        print(f"dir:\n{dir(each)}")
        print(f"each:\n{each.result}")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())