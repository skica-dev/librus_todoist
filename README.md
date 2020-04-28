# librus_todoist
Script that allows to sync Librus (biggest polish online gradebook) messages to Todoist's Inbox.
![Preview](https://imgur.com/tjww2AR.png)
Because attendance in my school during COVID outbreak is mandatory and based on whether we read messages durning lessons, this script makes them read and syncs them to Todoist's Inbox, the service that I use to manage my tasks. Then I can sometimes review them for tasks and mark as completed. This makes everything so easier!

Based on brilliant [LibrusTricks](https://github.com/kpostekk/Librus-Tricks) library by [@kpostekk](https://github.com/kpostekk) and [todoist-python](https://github.com/Doist/todoist-python).
## Setup
**This requires Librus Portal account connected to Librus Synergia account and same password for both accounts!**
**You also need premium account on Todoist to get messages' content as a comment in task. There is, hovewer, a free trial available and 70% student discount.** 
You need python3 and pipenv installed.
1. Create .env file based on .env.example (you may need to turn on hidden files visibility).
```
LIBRUS_USERNAME=kontolibrusportal
LIBRUS_PASSWORD=kochamlibrus!
CALENDAR_URL=https://nextcloud.com/remote.php/dav/
CALENDAR_USERNAME=admin
CALENDAR_PASSWORD=qweasd
CALENDAR_NAME=School
TODOIST_API_KEY=000000
```
2. I use Pipenv to manage requirements so you need it installed. Then this creates virtual environment for you and installs all dependencies.
```
pipenv install
```
3. On Libux add this to your crontab (*you have to edit directory path*), preferably using:
```
> crontab -e
*/5 * * * * cd /home/m4k5/librus_sync && /usr/local/bin/pipenv run python3 main.py messages >> /tmp/libr_mess.out
```
Windows and MacOS are supported, but you have to find out yourself how to set this up.
**I am not affilated with Librus in any way. You are using this at your own responsibility.**
