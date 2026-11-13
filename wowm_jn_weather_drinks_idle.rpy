# jn_weather_drinks_idle.rpy
# Just Natsuki 1.3.5-compatible weather drink idle submod
# Corrected full replacement with desk auto-scale/positioning.
#
# Install this file as:
#   game/Submods/wowm_jn_weather_drinks_idle/jn_weather_drinks_idle.rpy
#
# Required assets, preferred names:
#   game/Submods/wowm_jn_weather_drinks_idle/assets/hot_chocolate.png
#   game/Submods/wowm_jn_weather_drinks_idle/assets/strawberry_cream_milkshake.png
#
# Optional milkshake fallback name also supported:
#   game/Submods/wowm_jn_weather_drinks_idle/assets/milkshake.png
#
# Test with the debug button or console:
#   jump idle_weather_hot_chocolate
#   jump idle_weather_milkshake
#
# This file uses spaces only. Do not paste tabs into it. Use 4 spaces per indent.

init -10 python:
    import datetime
    import store

    # -------------------------------------------------------------------------
    # Safe constants/fallbacks
    # -------------------------------------------------------------------------

    if not hasattr(store, "JN_BLACK_ZORDER"):
        store.JN_BLACK_ZORDER = 100

    if not hasattr(store, "JN_PROP_ZORDER"):
        store.JN_PROP_ZORDER = 10

    if "drawer" not in globals():
        drawer = None

    # -------------------------------------------------------------------------
    # Asset paths with safe fallback support
    # -------------------------------------------------------------------------

    JN_WD_ASSET_DIR = "Submods/wowm_jn_weather_drinks_idle/assets/"

    JN_WD_HOT_CHOCOLATE_IMAGE_PATH = JN_WD_ASSET_DIR + "wowm_hot_choco.png"

    JN_WD_MILKSHAKE_IMAGE_PATH = JN_WD_ASSET_DIR + "wowm_strawberry_cream_milkshake.png"
    if not renpy.loadable(JN_WD_MILKSHAKE_IMAGE_PATH):
        if renpy.loadable(JN_WD_ASSET_DIR + "milkshake.png"):
            JN_WD_MILKSHAKE_IMAGE_PATH = JN_WD_ASSET_DIR + "milkshake.png"

    # -------------------------------------------------------------------------
    # Persistent setup
    # -------------------------------------------------------------------------

    if not hasattr(persistent, "jn_weather_drinks_enabled") or persistent.jn_weather_drinks_enabled is None:
        persistent.jn_weather_drinks_enabled = True

    # Important fix: this variable may exist but be None from an earlier test.
    if not hasattr(persistent, "jn_weather_drinks_last_day") or not isinstance(persistent.jn_weather_drinks_last_day, dict):
        persistent.jn_weather_drinks_last_day = {}

    if not hasattr(persistent, "jn_weather_drinks_last_weather") or persistent.jn_weather_drinks_last_weather is None:
        persistent.jn_weather_drinks_last_weather = "unknown"

    # -------------------------------------------------------------------------
    # Settings
    # -------------------------------------------------------------------------

    # Set these to False if you want the drinks to repeat more than once per day.
    JN_WD_HOT_CHOCOLATE_ONCE_PER_DAY = False
    JN_WD_MILKSHAKE_ONCE_PER_DAY = False

    # Daytime fallback: 6 AM to 6 PM.
    JN_WD_DAY_START_HOUR = 6
    JN_WD_DAY_END_HOUR = 18

    # -------------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------------

    def jn_wd_now():
        return datetime.datetime.now()

    def jn_wd_today_key():
        return jn_wd_now().strftime("%Y-%m-%d")

    def jn_wd_reset_last_day_if_needed():
        if not hasattr(persistent, "jn_weather_drinks_last_day") or not isinstance(persistent.jn_weather_drinks_last_day, dict):
            persistent.jn_weather_drinks_last_day = {}

    def jn_wd_is_daytime():
        hour = jn_wd_now().hour
        return JN_WD_DAY_START_HOUR <= hour < JN_WD_DAY_END_HOUR

    def jn_wd_get_weather_text():
        try:
            if store.jn_atmosphere.isCurrentWeatherSnow():
                return "snow"

            if store.jn_atmosphere.isCurrentWeatherThunder():
                return "rain"

            if store.jn_atmosphere.isCurrentWeatherRain():
                return "rain"

            if store.jn_atmosphere.isCurrentWeatherSunny():
                return "sunny"

            weather_type = store.jn_atmosphere.current_weather.weather_type

            if weather_type == store.jn_atmosphere.JNWeatherTypes.overcast:
                return "cloudy"

        except Exception:
            pass

        return "unknown"

    def jn_wd_was_done_today(drink_name):
        jn_wd_reset_last_day_if_needed()
        return persistent.jn_weather_drinks_last_day.get(drink_name) == jn_wd_today_key()

    def jn_wd_mark_done_today(drink_name):
        jn_wd_reset_last_day_if_needed()
        persistent.jn_weather_drinks_last_day[drink_name] = jn_wd_today_key()

    def jn_wd_hot_chocolate_condition():
        if not persistent.jn_weather_drinks_enabled:
            return False

        if JN_WD_HOT_CHOCOLATE_ONCE_PER_DAY and jn_wd_was_done_today("hot_chocolate"):
            return False

        weather = jn_wd_get_weather_text()

        if weather in ("rain", "snow", "cloudy"):
            persistent.jn_weather_drinks_last_weather = weather
            return True

        return False

    def jn_wd_milkshake_condition():
        if not persistent.jn_weather_drinks_enabled:
            return False

        if JN_WD_MILKSHAKE_ONCE_PER_DAY and jn_wd_was_done_today("milkshake"):
            return False

        weather = jn_wd_get_weather_text()

        if weather == "sunny" and jn_wd_is_daytime():
            persistent.jn_weather_drinks_last_weather = weather
            return True

        return False

    def jn_wd_safe_conclude_idle():
        try:
            import store.jn_idles as jn_idles
            jn_idles._concludeIdle()
        except Exception:
            return
    def jn_wd_hide_drinks():
        try:
            renpy.hide("prop", layer="master")
        except Exception:
            pass


# -----------------------------------------------------------------------------
# Image definitions
# -----------------------------------------------------------------------------

image jn_wd_hot_chocolate = Image(JN_WD_HOT_CHOCOLATE_IMAGE_PATH)
image jn_wd_milkshake = Image(JN_WD_MILKSHAKE_IMAGE_PATH)

# Auto-scale/desk placement transform.
# Adjust zoom/xpos/ypos here if your specific test sprites need fine tuning.
transform jn_wd_idle_drink_anim:
    # Anchored to the lower desk plane instead of free-floating screen coordinates.
    # No bobbing/movement. Adjust yoffset only if your desk background differs.
    zoom 1.0
    anchor (0.5, 1.0)
    xalign 0.50
    yalign 1.0
    yoffset 1.0
    alpha 1.0

image natsuki drinks_sippy:
    block:
        choice:
            "natsuki 4ucsdv"
            pause 4
            "natsuki 4ndwdr"
            pause 3
            "natsuki 4uchts"
            pause 4
            "natsuki 1kcssseaf"
            pause 3

        choice:
            "natsuki 4cspts"
            pause 4
            "natsuki 1udwpu"
            pause 3
            "natsuki 4fpltsedz"
            pause 4
            "natsuki 1ucsdv"
            pause 3


    repeat


# -----------------------------------------------------------------------------
# Idle registration
# -----------------------------------------------------------------------------

init 6 python:
    try:
        import store.jn_affinity as jn_affinity
        import store.jn_idles as jn_idles

        try:
            _jn_wd_idle_type = jn_idles.JNIdleTypes.vibing
        except Exception:
            _jn_wd_idle_type = None

        try:
            jn_idles._m1_script0x2didles__registerIdle(jn_idles.JNIdle(
                label="idle_weather_hot_chocolate",
                idle_type=_jn_wd_idle_type,
                affinity_range=(jn_affinity.NORMAL, None),
                conditional="jn_wd_hot_chocolate_condition()"
            ))
        except Exception as e:
            try:
                store.jn_utils.log("Weather Drinks: could not register hot chocolate idle: {0}".format(e))
            except Exception:
                pass

        try:
            jn_idles._m1_script0x2didles__registerIdle(jn_idles.JNIdle(
                label="idle_weather_milkshake",
                idle_type=_jn_wd_idle_type,
                affinity_range=(jn_affinity.NORMAL, None),
                conditional="jn_wd_milkshake_condition()"
            ))
        except Exception as e:
            try:
                store.jn_utils.log("Weather Drinks: could not register milkshake idle: {0}".format(e))
            except Exception:
                pass

    except Exception as e:
        try:
            store.jn_utils.log("Weather Drinks: idle registration skipped: {0}".format(e))
        except Exception:
            pass


# -----------------------------------------------------------------------------
# test
# -----------------------------------------------------------------------------



# -----------------------------------------------------------------------------
# Hot chocolate idle
# -----------------------------------------------------------------------------

label idle_weather_hot_chocolate:
    $ jn_wd_mark_done_today("hot_chocolate")
    $ Natsuki.setInConversation(True)
    $ renpy.restart_interaction()
    show black zorder JN_BLACK_ZORDER with Dissolve(0.5)
    show natsuki 1ullbo
    hide black with Dissolve(0.5)

    if persistent.jn_weather_drinks_last_weather == "snow":
        n 4ullaj "...It's snowing now, huh?"
        n 2fcscs "Mhmmmm. "
        extend 4fspbg "This calls for something warm."
    else:
        n 1ullbo "...Oh, is it raining?"
        extend 2fcssm " Hm.{w=0.2} Then I'm getting something warm."

    n 2fsqsm "And not just plain hot chocolate, either."
    n 2fchbg "With whipped cream and marshmallows."
    extend " Obviously."
    n 1uchsm "I'll be right back!"

    show black zorder JN_BLACK_ZORDER with Dissolve(0.5)
    show jn_wd_hot_chocolate at jn_wd_idle_drink_anim zorder JN_PROP_ZORDER
    show natsuki 1fchsmeme
    play audio drawer
    hide black with Dissolve(0.5)

    n 1fchbg "There we go!"
    n 2fsqsm "Chocolate,{w=0.2} whipped cream,{w=0.2} marshmallows...{w=0.5}{nw}"
    extend " yep."
    n 4fwlbg "Bad weather is way easier to deal with like this."

    window hide
    show natsuki drinks_sippy
    $ jnClickToContinue()
    $ random_response = renpy.random.randint(1, 2)

    if random_response == 1:
        n 1uchsm "Mmm..."
        extend 2ucsts " that was soo good."
        n 2fcsss "I guess rain and snow aren't completely terrible when I have something like this."
        n 4nsrbg "I'm gonna put this away before I start wanting another one."

    elif random_response == 2:
        n "Days like this are made for hot chocolate."
        n "Not that I've been thinking about it all day or anything...{w=0.9}{nw}"
        extend " okay,{w=0.3} maybe {cps=17}jusstt{/cps} a little."
        n "Better put it away before I get too comfortable and ask for more."

    elif random_response == 3:
        if Natsuki.isLove(higher=True):
            $ chosen_tease = jn_utils.getRandomTease()
            $ chosen_endearment = jn_utils.getRandomEndearment()
            n "Ahhh...[w=0.4]{nw}"
            extend " that hits the spot."
            n "Whatever's going on outside, this makes it so much more tolerable."
            n "...{w=0.4}You make it better too,[w=0.6] [chosen_tease],{w=0.67}{nw}"
            extend " ehehe."
            n "Though...{w=0.4} I should stop here.{w=0.6}{nw}"
            extend " Otherwise I'll want another one,{w=0.7}{nw}"
            extend " and then another."

        elif Natsuki.isEnamored(higher=True):
            n "Better put this down now,{w=0.78}{nw}"
            extend " or I'll be wanting another before long."

        elif Natsuki.isHappy(higher=True):
            n "Cold weather,{w=0.4}{nw}"
            extend " warm drink {w=0.5}{nw}"
            extend "...{w=0.4}and you hovering around...{w=0.6}"
            n "...{w=0.4}It's not terrible."
            n "Anyways,{w=0.3} away it goes —{w=0.67}{nw}"
            extend " before I want another."

    show black zorder JN_BLACK_ZORDER with Dissolve(0.5)
    hide jn_wd_hot_chocolate
    hide prop jn_wd_hot_chocolate
    play audio drawer
    show natsuki 1fchsmeme
    hide black with Dissolve(0.5)

    n 1unmbo "Okay, I'm back."
    $ jn_wd_safe_conclude_idle()
    return


# -----------------------------------------------------------------------------
# Strawberry and cream milkshake idle
# -----------------------------------------------------------------------------

label idle_weather_milkshake:
    $ jn_wd_mark_done_today("milkshake")
    $ Natsuki.setInConversation(True)
    $ renpy.restart_interaction()


    show black zorder JN_BLACK_ZORDER with Dissolve(0.5)
    show natsuki 1ullbo
    hide black with Dissolve(0.5)

    n 1ullss "It's actually pretty nice out right now."
    n 2fchbg "Sunny weather means I get to have something cold and sweet."
    n 2fsqsm "A strawberry and cream milkshake sounds perfect..."
    n 2fchsm "With just a dash of chocolate, obviously."
    n 1uchbg "I'll grab one really quick!"

    show black zorder JN_BLACK_ZORDER with Dissolve(0.5)
    show jn_wd_milkshake at jn_wd_idle_drink_anim zorder JN_PROP_ZORDER
    show natsuki 1fchsmeme
    play audio drawer
    hide black with Dissolve(0.5)

    n 1fchbg "Okay, now this looks good."
    n 2fcssm "Strawberry, cream, and just enough chocolate to make it better."
    n 2fsqsm "Don't get jealous."

    window hide
    show natsuki drinks_sippy
    $ jnClickToContinue()

    n 1uchsm "Mmm... that was really good."
    n 2fcsss "Cold, sweet, and not too heavy."
    n 2fsqsm "I'm putting it away before I get brain freeze."

    show black zorder JN_BLACK_ZORDER with Dissolve(0.5)
    hide jn_wd_milkshake
    hide prop jn_wd_milkshake
    play audio drawer
    show natsuki 1fchsmeme
    hide black with Dissolve(0.5)

    n 1unmbo "Alright, I'm done."
    $ jn_wd_safe_conclude_idle()
    return


# -----------------------------------------------------------------------------
# Debug/helper labels
# -----------------------------------------------------------------------------

label jn_weather_drinks_force_clear:
    $ jn_wd_reset_last_day_if_needed()
    hide jn_wd_hot_chocolate
    hide prop jn_wd_hot_chocolate
    hide jn_wd_milkshake
    hide prop jn_wd_milkshake
    $ renpy.notify("Drink cleared.")
    return


label jn_weather_drinks_reset_daily_lock:
    $ persistent.jn_weather_drinks_last_day = {}
    $ renpy.notify("Daily drink lock reset.")
    return
