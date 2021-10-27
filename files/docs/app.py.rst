======
app.py
======

--------------------------------
Retrieve security zones from SRX
--------------------------------

We will be using Scrapli to issue an RPC call to our firewalls to receive information regarding the device's security zones.

This project has an example for both synchronous and asynchronous communications, `app.py` and `app_sync.py` respectively.

-----------
Explanation
-----------

.. code-block:: python

    import asyncio
    import xmltodict

    from scrapli_netconf.driver import AsyncNetconfDriver
    from scrapli.logging import enable_basic_logging
    from jinja2 import Environment, FileSystemLoader


We need to import some functionality into our script:
  - `asyncio` will enable our script to be executed in an async, non-io blocking manner
  - `xmltodict` will simplify the conversion of our XML object into a Python dictionary object
  - `AsyncNetconfDriver` is our primary method of interacting with Scrapli's transport system
  - `enable_basic_logging` will write simple logs to the localhost
  - `jinja2` is our way of templating the output into something more appropriate for a file


.. code-block:: python

    # Enable logging. Create a log file in the current directory.
    enable_basic_logging(file=True, level="debug")


We want to turn on logging right out the gate, so we call the imported `enable_basic_logging` method after passing in two parameters: `file` and `level`


.. code-block:: python

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


We take this opportunity to create some objects that define our parameters.
  - define two network devices, `GALVESTON` and `SANANTONIO`
  - create a new list called `DEVICES` and place these two devices in there
  - our request for information on the security zones is embedded in an object called `RPC`


.. code-block:: python

    # jinja2 parameters
    env = Environment(loader=FileSystemLoader('templates'),trim_blocks=True)
    template = env.get_template('test.j2')


We will want to write the output to a file, but we can do ourselves a favor by running the output through a template engine first. We will use Jinja2 parameters to tell the script where to find
  - the template folder
  - trim the empty white spaces
  - which template file to run our response through 


.. code-block:: python

    async def gather_security_zones(device):
        conn = AsyncNetconfDriver(**device)
        await conn.open()
        result = await conn.rpc(filter_=RPC)
        await conn.close()
        return result


Here we define our asynchronous function that will handle the connections to our network devices.
  - we create an object called `conn` that will store our connection parameters into the `AsyncNetconfDriver`
  - our connections are opened and we `await` for the responses
  - the NETCONF API call `RPC` is sent to each open connection with the `rpc` method; response is stored as `result`
  - connections to our devices need to be closed, so we again use the `conn` object but this time with the `close` method
  - `result` is returned to the `main` function (defined below)


.. code-block:: python

    # primary function
    async def main():
        """Function to gather coroutines, await them and print results"""
        coroutines = [gather_security_zones(device) for device in DEVICES]
        results = await asyncio.gather(*coroutines)
        for each in results:
            reply_as_dict = xmltodict.parse(each.result)
            security_zones = reply_as_dict["rpc-reply"]["zones-information"]["zones-security"]

            # template output with jinja2 and save to file
            output_from_parsed_template = template.render(security_zones=security_zones)
            with open(f"./output/{each.host}.yaml", "w") as fh:
                fh.write(output_from_parsed_template)

    if __name__ == "__main__":
        asyncio.get_event_loop().run_until_complete(main())

