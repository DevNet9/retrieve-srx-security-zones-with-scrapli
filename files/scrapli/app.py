from scrapli_netconf import NetconfDriver

JUNOS_DEVICE = {
    "host": "192.168.105.137",
    "port": 22,
    "auth_username": "scrapli",
    "auth_password": "juniper123",
    "auth_strict_key": False,
    "transport": "system",
    "timeout_ops": 10,
    "timeout_transport": 10,
}

RPC = """
<get-zones-information>
</get-zones-information>
"""


def main():
    """Basic use example"""
    # create scrapli_netconf connection just like with scrapli, open the connection
    conn = NetconfDriver(**JUNOS_DEVICE)
    conn.open()
    print(conn.server_capabilities)

    # get some operational data via "rpc" for juniper style rpc calls; note the `filter_` to
    # not reuse builtins
    result = conn.rpc(filter_=RPC)
    print(result.result)
    # print(dir(result))

    # close the session
    conn.close()


if __name__ == "__main__":
    main()