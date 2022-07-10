# THIS REPOSITORY IS NOW ARCHIVED





# eAsistentDiscordBot
***
## Bot commands
<table>
<tbody>
  <tr>
    <td><b>command</b></td>
    <td><b>alias</b></td>
    <td><b>explanation</b></td>
  </tr>
  <tr>
    <td>urnik</td>
    <td>u</td>
    <td>prints the schedule</td>
  </tr>

</tbody>
</table>


***
<details>
    <summary>Setup</summary>

#### Seting up dependencies
if you are using [pipenv](https://github.com/pypa/pipenv)
    
    pipenv sync

if you are using [pip](https://github.com/pypa/pip)

    pip install -r requirements.txt

###
#### Setting up bot credentials and settings
* **run setup.py**
* insert your discord token into credentials.json > "BOT_TOKEN"
* insert your school_id into settings.json > "SCHOOL_ID"
* insert your class_id into settings.json > "CLASS_ID"
* insert the channel you want to have the schedule sent every day into 
  settings.json > "SCHEDULE_CHANNEL_ID"


<details>
  <summary>How to get school and class id</summary>

<!-- Not my school,
first school here https://dijaski.net/srednje-sole/srednje-sole-v-sloveniji -->

click print ![Click print image](https://i.imgur.com/lFiztdw.png)
* a popup window will open
* copy it's URL
* it will look something like 
https://www.easistent.com/urniki/izpis/94d50865b6c4d9553b4adc9a6942cb2af9926923/439113/...
* the first item after izpis/ is the school id, the second is the class id

![](https://i.imgur.com/hS6E5zf.png)
</details>

<details>
    <summary>How to get channel id</summary>

[Watch this tutorial](https://www.youtube.com/watch?v=YjiQ7CajAgg)


</details>

<details>
    <summary>How to create a discord bot and invite it to your server</summary>

* got to https://discord.com/developers/applications
* click "New Application" in the top right corner
* give your bot a name 
* click create
* click "Bot" in the left dropdown
* click "Add Bot" in the top right corner
* click "Yes, do it!"
* scroll down and enable "Message Content Intent"
![](https://i.imgur.com/ReMD5Gl.png)
* make sure that you save the changes
* click "OAuth2" the left dropdown then "URL Generator"
* in "SCOPES" select "bot" then "Read Messages/View Channels" and "Send Messages"
![](https://i.imgur.com/PXZZmWR.png)
* click copy and paste the URL into the URL bar then authorize your 
  application to the server you want it in

</details>
<details>
    <summary>How to get discord bot token</summary>

* In your application go to "Bot"
* click "Reset Token"

* copy the token and paste it into credentials.json


</details>
<details>
    <summary>Examples of settings.json and credentials.json</summary>

credentials.json
```json
{
    "BOT_TOKEN": "OTY1MjkzNDY4NjIyNjUxNDEz.YlxFmQ.6RBB2DMuFZ4GEo5uU9-5HPtE9_4"
}
```

settings.json
```json
{
    "SCHOOL_ID": "94d50865b6c4d9553b4adc9a6942cb2af9926923",
    "CLASS_ID": "439113",
    "SCHEDULE_CHANNEL_ID": "965156181372977162"

}
```

</details>
</details>

***
## Questions

If you have any questions open a 
[discussion on Github](https://github.com/PingWasFun/eAsistentDiscordBot/discussions/categories/general)
