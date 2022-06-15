import discord
import asyncpraw
import sqlite3
import datetime as dt
import matplotlib.pyplot as plt
import io

import config


reddit = asyncpraw.Reddit(
    client_id=config.PRAW_CLIENT,
    client_secret=config.PRAW_SECRET,
    user_agent=config.PRAW_USERAGENT
)

con = sqlite3.connect("database.db")
cur = con.cursor()


sub_ids = {
    935553013710483546: "minecraft_survival",
    935553034963001345: "mc_survival"
}


class Subcounter(discord.Client):
    def __init__(self):
        super().__init__()

    @staticmethod
    async def on_ready():
        print(f"{client.user} has connected to Discord!")

    @staticmethod
    async def on_message(message):
        if (m_id := message.channel.id) in sub_ids:
            if message.content.lower() == "chart":
                subreddit = await reddit.subreddit(sub_ids[m_id], fetch=True)  # 935553013710483546

                year, month, day = (int(x) for x in dt.datetime.today().strftime('%Y-%m-%d').split("-"))
                subs = subreddit.subscribers
                active = subreddit.active_user_count

                cur.execute(f"SELECT * FROM {sub_ids[m_id]}")
                rows = cur.fetchall()

                for y, m, d, s in rows:
                    if (year, month, day) == (y, m, d):
                        if subs == s:
                            break
                        else:
                            cur.execute(f"""
                                UPDATE {sub_ids[m_id]} SET subs = {s} WHERE year = {year} AND month = {month} AND day = {day}
                            """)
                            break
                else:
                    cur.execute(f"INSERT INTO {sub_ids[m_id]} VALUES ({year}, {month}, {day}, {subs})")
                con.commit()

                cur.execute(f"SELECT * FROM {sub_ids[m_id]}")
                rows = cur.fetchall()

                # Parse data
                data = []
                for y, m, d, s in rows:
                    data.append((dt.datetime(y, m, d), s))
                data = sorted(data, key=lambda x: x[0])[-7:]

                data_stream = io.BytesIO()

                # Plot graph
                plt.plot([x[0] for x in data], [x[1] for x in data])
                plt.gcf().autofmt_xdate()

                # Save content into the data stream
                plt.savefig(data_stream, format='png', bbox_inches="tight", dpi=80)

                data_stream.seek(0)
                chart = discord.File(data_stream, filename="subs_chart.png")

                embed = discord.Embed(title=f"{sub_ids[m_id]} sub counts of the last 7 registries")
                embed.add_field(name="Subs", value=str(subs), inline=True)
                embed.add_field(name="Active", value=str(active), inline=True)
                embed.set_image(url="attachment://subs_chart.png")

                plt.clf()

                await message.channel.send(embed=embed, file=chart)
        # if message.author.id == config.ADMIN_ID:
        #     await message.channel.send("Hello, John!")


client = Subcounter()
client.run(config.DISCORD_TOKEN)
