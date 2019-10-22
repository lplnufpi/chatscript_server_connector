# ChatScript Server Connector

ChatScript server receives TCP messages in its own protocol (see [ChatScript Protocol](https://github.com/ChatScript/ChatScript/blob/master/WIKI/CLIENTS-AND-SERVERS/ChatScript-ClientServer-Manual.md#chatscript-protocol)).
Thus, this code was created to simplify messaging between client and CS Server, and abstract the CS Protocol operation.

## How to use

You can use like shown below just creating the connection with the username, or specify `botname`, `ip` and `port`.

```python
from cs_connector import CSConnection
conn = CSConnection('username')
msg = conn.send('Hello')
print(msg)
```
