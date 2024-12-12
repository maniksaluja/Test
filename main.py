async def check_channel_access(client, channels):
    """
    Verify that the bot can send messages in the specified channels.
    """
    for channel_id in channels:
        if channel_id is None:
            print(f"Channel ID is None for {client.name}. Skipping.")
            continue
        try:
            msg = await client.send_message(channel_id, '.')
            await msg.delete()
        except Exception as e:
            print(f"Error accessing channel {channel_id} for {client.name}: {e}")
            return False, channel_id
    return True, None

async def start():
    """
    Start both bot clients and validate their access to required channels.
    """
    await app.start()
    await app1.start()
    
    channels_to_check = [
        DB_CHANNEL_ID,
        DB_CHANNEL_2_ID,
        AUTO_SAVE_CHANNEL_ID,
        LOG_CHANNEL_ID
    ] + FSUB

    # Check channel access for both bots
    app_status, app_failed_channel = await check_channel_access(app, channels_to_check)
    app1_status, app1_failed_channel = await check_channel_access(app1, FSUB)

    if not (app_status and app1_status):
        if not app_status:
            print(f"Bot @:91: failed to access channel: {app_failed_channel}")
        if not app1_status:
            print(f"Bot @:91-1: failed to access channel: {app1_failed_channel}")
        await app.stop()
        await app1.stop()
        sys.exit()

    bot1_info = await app.get_me()
    bot2_info = await app1.get_me()

    print(f'@{bot1_info.username} started.')
    print(f'@{bot2_info.username} started.')

    await idle()
