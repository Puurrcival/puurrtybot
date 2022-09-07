from discord import Embed

TEXT_RULES = """
Hello I'm **Officer Whiskers**. You must be new here?
Before you go any further let me tell you about our **RULES**:

:one: **Respect all members.**
Treat others with kind and respect like they would.

:two: **No spamming.**
This includes text walls, duplicate text, or any other form.

:three: **Do not advertise.**
Advertising other discord servers, items worth in real life currency.

:four: **Don't try to bypass the filter.**
We have a filter for a reason. Don't try to bypass the filter.

:five: **Keep all messages appropriate and relevant.**
Be respectful to everyone and be appropriate in chat.

:six: **No NSFW.**
Please do not post anything we may find to be NSFW content.

:seven: **Keep your name appropriate.**
Avoid inappropriate material in your username.

:eight: **Do not tag staff for no reason.**
Don't tag the staff if you don't have any questions or need any help.

:nine: **The staff team's word is final.**
If a staff member tells you to stop doing something, do it.

Do you agree with those rules?
If so it is time to meet your guide **Puurrdo**!

**Unfortunately he is missing, can you find Puurrdo?**
    """.strip()

RULES_EMBED = Embed(title="Welcome to Puurrty Cats Society!", description=TEXT_RULES, color=0x109319)
RULES_EMBED.set_thumbnail(url=f"""https://image-optimizer.jpgstoreapis.com/QmZHdzWXyXMVSUNQRhNyYeQKyaQ8qMZStAQUZAmhJsTzfN""")


TEXT_VERIFY = """
Hello I'm **Abe**. I want you to improve your citizenship!

**Verify Wallet**
Registered cats grant you special access and rewards.

**Verify Twitter**
Becoming an influencuurr grants you special access and rewards.

**Verify Poker**
This feautre is coming soon.
    """.strip()

VERIFY_EMBED = Embed(title="Welcome to the registration office!", description=TEXT_VERIFY, color=0x109319)
VERIFY_EMBED.set_thumbnail(url=f"""https://image-optimizer.jpgstoreapis.com/QmXBGsPVnpjVJCfBaCfuGYj1akynUx7N8vjdqkiZa3PJZQ""")
# Poker: https://www.pokernow.club/mtt/puurrtybot-53lMD8bXp9