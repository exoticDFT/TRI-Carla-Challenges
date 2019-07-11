import carla

def create(host='127.0.0.1', port=2000, timeout=3.0):
    '''
    Creates a Carla client to be used in a Carla runtime script.

    Parameters
    ----------
    host : str, optional
        The string containing the host address.
    port : int, optional
        The port in which the client will connect.
    timeout : float, optional
        The time in which to wait for a response from the server.

    Returns
    -------
    carla.Client
        A Carla client that is connected to the provided server.
    '''
    client = carla.Client(host, port)
    client.set_timeout(timeout)

    return client