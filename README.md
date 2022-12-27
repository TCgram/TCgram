<p align="center">
    <a href="https://github.com/TCgram/TCgram">
        <img src="https://docs.TCgram.com/_static/TCgram.png" alt="TCgram" width="128">
    </a>
    <br>
    <b>Telegram MTProto API Framework for Python</b>
    <br>
    <a href="https://TCgram.com">
        Homepage
    </a>
    •
    <a href="https://docs.TCgram.com">
        Documentation
    </a>
    •
    <a href="https://docs.TCgram.com/releases">
        Releases
    </a>
    •
    <a href="https://t.me/TCdgram">
        News
    </a>
</p>

## TCgram

> Elegant, modern and asynchronous Telegram MTProto API framework in Python for users and bots

``` python
from TCgram import Client, filters

app = Client("my_account")


@app.on_message(filters.private)
async def hello(client, message):
    await message.reply("Hello from TCgram!")


app.run()
```

### Installing

``` bash
pip3 install TCgram
```
