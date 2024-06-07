import random

from graphics import *

win = GraphWin("Make your own subway sandwich!", 950, 600)
win.setBackground("powderblue")

# Container for buttons
# When you make a new button, append it to this this list.
# Then later on, when you're checking for clicks, you can loop through this list
BUTTON_LIST = []
CLICK_COUNTER = 0


def hi(win):
    clickpoint = win.getMouse()


def main_page(win):
    global CLICK_COUNTER
    win.setBackground("powderblue")

    # Title
    title = Text(Point(475, 30), "Make your own subway sandwich!")
    title.setSize(40)
    title.setStyle("bold")
    title.setTextColor("pink")
    title.draw(win)

    # Sandwich
    bread1 = make_rectangle(Point(300, 75), Point(700, 100), colour="navajowhite")
    bread2 = make_rectangle(Point(300, 205), Point(700, 230), colour="navajowhite")
    sauce = make_rectangle(Point(285, 115), Point(715, 100), colour="darkgray")
    vegetable1 = make_rectangle(Point(275, 140), Point(725, 115), colour="darkgray")
    vegetable2 = make_rectangle(Point(265, 165), Point(735, 140), colour="darkgray")
    cheese = make_rectangle(Point(300, 180), Point(700, 165), colour="darkgray")
    meat = make_rectangle(Point(265, 205), Point(735, 180), colour="darkgray")

    # Ingredient boxes
    meatbox = make_rectangle(Point(50, 580), Point(200, 260), colour="pink")
    cheesebox = make_rectangle(Point(225, 440), Point(375, 260), colour="pink")
    vegetablebox1 = make_rectangle(Point(400, 475), Point(550, 260), colour="pink")
    vegetablebox2 = make_rectangle(Point(575, 475), Point(725, 260), colour="pink")
    saucebox = make_rectangle(Point(750, 570), Point(900, 260), colour="pink")

    meatboxtext = place_label_text(Point(125, 290), "Meat:")
    cheeseboxtext = place_label_text(Point(300, 290), "Cheese:")
    vegetablebox1text = place_label_text(Point(475, 290), "Vegetable 1:")
    vegetablebox2text = place_label_text(Point(650, 290), "Vegetable 2:")
    sauceboxtext = place_label_text(Point(825, 290), "Sauce:")

    # Meat
    legham_button, legham, leghamtext = draw_ingredient(
        insertion_point=Point(85, 320),
        active_radius=20,
        ingredient_radius=11,
        ingredient_colour="lightpink",
        lable_text="Leg Ham",
        label_text_offset=25,
        text_size=10,
    )

    schnitzel_button, schnitzel, schnitzeltext = draw_ingredient(
        insertion_point=Point(165, 320),
        ingredient_colour="chocolate3",
        lable_text="Schnitzel",
    )

    salami_button, salami, salamitext = draw_ingredient(
        insertion_point=Point(85, 375),
        active_radius=20,
        ingredient_colour="firebrick1",
        lable_text="Salami",
    )

    turkey_button, turkey, turkeytext = draw_ingredient(
        insertion_point=Point(165, 375),
        ingredient_colour="cornsilk",
        lable_text="Turkey",
    )

    tuna_button, tuna, tunatext = draw_ingredient(
        insertion_point=Point(85, 430),
        ingredient_colour="burlywood2",
        lable_text="Tuna",
    )

    meatball_button, meatball, meatballtext = draw_ingredient(
        insertion_point=Point(165, 430),
        active_radius=20,
        ingredient_colour="brown3",
        lable_text="Meatball",
    )

    grilledchicken_button, grilledchicken, grilledchickentext = draw_ingredient(
        insertion_point=Point(85, 482.5),
        active_radius=20,
        ingredient_colour="bisque1",
        lable_text="Grilled Chicken",
        text_size=7,
    )

    roastbeef_button, roastbeef, roastbeeftext = draw_ingredient(
        insertion_point=Point(165, 482.5),
        active_radius=20,
        ingredient_colour="antiquewhite4",
        lable_text="Roast Beef",
        text_size=8,
    )

    bbqpulledpork_button, bbqpulledpork, bbqpulledporktext = draw_ingredient(
        insertion_point=Point(85, 535),
        active_radius=20,
        ingredient_colour="burlywood4",
        lable_text="BBQ Pulled Pork",
        text_size=6,
    )

    veggiepattie_button, veggiepattie, veggiepattietext = draw_ingredient(
        insertion_point=Point(167.5, 535),
        active_radius=20,
        ingredient_colour="sandybrown",
        lable_text="Veggie Pattie",
        text_size=7,
    )

    # Cheese
    oldenglish_button, oldenglish, oldenglishtext = draw_ingredient(
        insertion_point=Point(265, 331.7),
        active_radius=20,
        ingredient_colour="gold",
        lable_text="Old English",
        text_size=10,
    )

    cheddar_button, cheddar, cheddartext = draw_ingredient(
        insertion_point=Point(335, 331.7),
        active_radius=20,
        ingredient_colour="oldlace",
        lable_text="Cheddar",
    )

    mozzarella_button, mozzarella, mozzarellatext = draw_ingredient(
        insertion_point=Point(265, 390),
        active_radius=20,
        ingredient_colour="palegoldenrod",
        lable_text="Mozzarella",
    )

    swiss_button, swiss, swisstext = draw_ingredient(
        insertion_point=Point(335, 390),
        ingredient_colour="lightgoldenrodyellow",
        lable_text="Swiss",
    )

    # First vegetable
    lettuce1_button, lettuce1, lettuce1text = draw_ingredient(
        insertion_point=Point(430, 322.5),
        ingredient_colour="DarkOliveGreen1",
        lable_text="Lettuce1",
    )

    tomato1_button, tomato1, tomato1text = draw_ingredient(
        insertion_point=Point(510, 325),
        ingredient_colour="tomato",
        lable_text="Tomato1",
    )

    onion1_button, onion1, onion1text = draw_ingredient(
        insertion_point=Point(430, 375),
        ingredient_colour="plum1",
        lable_text="Onion1",
    )

    carrot1_button, carrot1, carrot1text = draw_ingredient(
        insertion_point=Point(512.5, 372.5),
        active_radius=17,
        ingredient_colour="orange",
        lable_text="Carrot1",
    )

    spinach1_button, spinach1, spinach1text = draw_ingredient(
        insertion_point=Point(427.5, 432.5),
        active_radius=20,
        ingredient_colour="darkgreen",
        lable_text="Spinach1",
        text_size=8,
    )

    olive1_button, olive1, olive1text = draw_ingredient(
        insertion_point=Point(510, 429),
        ingredient_radius=9,
        ingredient_colour="grey13",
        lable_text="Olive1",
    )

    # Second Vegetable
    lettuce2_button, lettuce2, lettuce2text = draw_ingredient(
        insertion_point=Point(605, 322.5),
        ingredient_colour="DarkOliveGreen1",
        lable_text="Lettuce2",
    )

    tomato2_button, tomato2, tomato2text = draw_ingredient(
        insertion_point=Point(685, 325),
        ingredient_colour="tomato",
        lable_text="Tomato2",
    )

    onion2_button, onion2, onion2text = draw_ingredient(
        insertion_point=Point(605, 375), ingredient_colour="plum1", lable_text="Onion2"
    )

    carrot2_button, carrot2, carrot2text = draw_ingredient(
        insertion_point=Point(687.5, 372.5),
        active_radius=17,
        ingredient_colour="orange",
        lable_text="Carrot2",
    )

    spinach2_button, spinach2, spinach2text = draw_ingredient(
        insertion_point=Point(607.5, 427.5),
        active_radius=17,
        ingredient_colour="darkgreen",
        lable_text="Spinach2",
    )

    olive2_button, olive2, olive2text = draw_ingredient(
        insertion_point=Point(685, 429),
        ingredient_radius=9,
        ingredient_colour="grey13",
        lable_text="Olive2",
    )

    # Sauce

    ketchup_button, ketchup, ketchuptext = draw_ingredient(
        insertion_point=Point(785, 325),
        ingredient_colour="orangered",
        lable_text="Ketchup",
    )

    mayo_button, mayo, mayotext = draw_ingredient(
        insertion_point=Point(865, 325), ingredient_colour="cornsilk", lable_text="Mayo"
    )

    chipotle_button, chipotle, chipotletext = draw_ingredient(
        active_radius=20,
        insertion_point=Point(785, 375),
        ingredient_colour="sandybrown",
        lable_text="Chipotle",
    )

    bbq_button, bbq, bbqtext = draw_ingredient(
        active_radius=17,
        insertion_point=Point(865, 374),
        ingredient_colour="orangered4",
        lable_text="BBQ",
    )

    sweetchilli_button, sweetchilli, sweetchillitext = draw_ingredient(
        active_radius=17,
        insertion_point=Point(785, 425),
        ingredient_colour="orangered3",
        lable_text="Sweet Chilli",
        text_size=8,
    )

    ranch_button, ranch, ranchtext = draw_ingredient(
        active_radius=17,
        insertion_point=Point(865, 425),
        ingredient_colour="ghostwhite",
        lable_text="Ranch",
    )

    honeymustard_button, honeymustard, honeymustardtext = draw_ingredient(
        insertion_point=Point(785, 475),
        active_radius=20,
        ingredient_colour="gold2",
        lable_text="Honey Mustard",
        text_size=7,
    )

    aioli_button, aioli, aiolitext = draw_ingredient(
        insertion_point=Point(865, 475),
        active_radius=20,
        ingredient_colour="wheat1",
        lable_text="Aioli",
    )

    hotsauce_button, hotsauce, hotsaucetext = draw_ingredient(
        insertion_point=Point(830, 530),
        active_radius=20,
        ingredient_colour="orangered2",
        lable_text="Hot Sauce",
        text_size=8,
    )

    # Information
    helpbox = make_rectangle(Point(800, 150), Point(870, 100), colour="orange2")
    helptext = place_label_text(Point(835, 125), "HELP", size=17)
    # Toasted
    toastedtext = place_label_text(Point(90, 125), "Toasted?", size=17)

    yes_button, yes, yestext = draw_ingredient(
        ingredient_colour="sandybrown",
        insertion_point=Point(50, 175),
        active_radius=30,
        ingredient_radius=30,
        lable_text="YES",
        text_size=15,
        label_text_offset=0,
    )

    no_button, no, notext = draw_ingredient(
        ingredient_colour="navajowhite",
        insertion_point=Point(130, 175),
        active_radius=30,
        ingredient_radius=30,
        lable_text="NO",
        text_size=15,
        label_text_offset=0,
    )

    # Reset
    resetbox_button, resetbox, resetboxtext = draw_ingredient(
        ingredient_colour="darkgray",
        active_radius=30,
        ingredient_radius=30,
        insertion_point=Point(835, 200),
        lable_text="RESET",
        label_text_offset=0,
    )

    clicksbox = make_rectangle(Point(290, 580), Point(580, 520), colour="Light green")
    clicksnumber = place_label_text(
        Point(520, 551), CLICK_COUNTER, size=40, textcolor="black", style="normal"
    )
    clickstext = place_label_text(
        Point(400, 550), "Clicks:", size=40, textcolor="black", style="normal"
    )

    while True:
        click_point = win.getMouse()
        print(click_point)
        CLICK_COUNTER += 1
        clicksnumber.setText(CLICK_COUNTER)

        x = click_point.getX()
        y = click_point.getY()

        if (x >= 800 and x <= 870) and (y <= 150 and y >= 100):
            title.undraw()
            bread1.undraw()
            bread2.undraw()
            sauce.undraw()
            vegetable1.undraw()
            vegetable2.undraw()
            cheese.undraw()
            meat.undraw()
            meatboxtext.undraw()
            cheeseboxtext.undraw()
            vegetablebox1text.undraw()
            vegetablebox2text.undraw()
            sauceboxtext.undraw()
            legham_button.undraw()
            legham.undraw()
            leghamtext.undraw()
            schnitzel_button.undraw()
            schnitzel.undraw()
            schnitzeltext.undraw()
            salami_button.undraw()
            salami.undraw()
            salamitext.undraw()
            turkey_button.undraw()
            turkey.undraw()
            turkeytext.undraw()
            tuna_button.undraw()
            tuna.undraw()
            tunatext.undraw()
            meatball_button.undraw()
            meatball.undraw()
            meatballtext.undraw()
            grilledchicken_button.undraw()
            grilledchicken.undraw()
            grilledchickentext.undraw()
            roastbeef_button.undraw()
            roastbeef.undraw()
            roastbeeftext.undraw()
            bbqpulledpork_button.undraw()
            bbqpulledpork.undraw()
            bbqpulledporktext.undraw()
            veggiepattie_button.undraw()
            veggiepattie.undraw()
            veggiepattietext.undraw()
            meatbox.undraw()
            oldenglish_button.undraw()
            oldenglish.undraw()
            oldenglishtext.undraw()
            cheddar_button.undraw()
            cheddar.undraw()
            cheddartext.undraw()
            mozzarella_button.undraw()
            mozzarella.undraw()
            mozzarellatext.undraw()
            swiss_button.undraw()
            swiss.undraw()
            swisstext.undraw()
            cheesebox.undraw()
            lettuce1_button.undraw()
            lettuce1.undraw()
            lettuce1text.undraw()
            tomato1_button.undraw()
            tomato1.undraw()
            tomato1text.undraw()
            onion1_button.undraw()
            onion1.undraw()
            onion1text.undraw()
            carrot1_button.undraw()
            carrot1.undraw()
            carrot1text.undraw()
            spinach1_button.undraw()
            spinach1.undraw()
            spinach1text.undraw()
            olive1_button.undraw()
            olive1.undraw()
            olive1text.undraw()
            vegetablebox1.undraw()
            lettuce2_button.undraw()
            lettuce2.undraw()
            lettuce2text.undraw()
            tomato2_button.undraw()
            tomato2.undraw()
            tomato2text.undraw()
            onion2_button.undraw()
            onion2.undraw()
            onion2text.undraw()
            carrot2_button.undraw()
            carrot2.undraw()
            carrot2text.undraw()
            spinach2_button.undraw()
            spinach2.undraw()
            spinach2text.undraw()
            olive2_button.undraw()
            olive2.undraw()
            olive2text.undraw()
            vegetablebox2.undraw()
            ketchup_button.undraw()
            ketchup.undraw()
            ketchuptext.undraw()
            mayo_button.undraw()
            mayo.undraw()
            mayotext.undraw()
            chipotle_button.undraw()
            chipotle.undraw()
            chipotletext.undraw()
            bbq_button.undraw()
            bbq.undraw()
            bbqtext.undraw()
            sweetchilli_button.undraw()
            sweetchilli.undraw()
            sweetchillitext.undraw()
            ranch_button.undraw()
            ranch.undraw()
            ranchtext.undraw()
            honeymustard_button.undraw()
            honeymustard.undraw()
            honeymustardtext.undraw()
            aioli_button.undraw()
            aioli.undraw()
            aiolitext.undraw()
            hotsauce_button.undraw()
            hotsauce.undraw()
            hotsaucetext.undraw()
            saucebox.undraw()
            helpbox.undraw()
            helptext.undraw()
            toastedtext.undraw()
            yes_button.undraw()
            yes.undraw()
            yestext.undraw()
            no_button.undraw()
            no.undraw()
            notext.undraw()
            resetbox_button.undraw()
            resetbox.undraw()
            resetboxtext.undraw()
            clicksbox.undraw()
            clicksnumber.undraw()
            clickstext.undraw()
            helppage(win)

        for button in BUTTON_LIST:
            if (
                distance(button["insertion_point"], click_point)
                < button["active_radius"]
            ):
                print(f"Clicked on {button['ingredient']}")
                ingredient = button["ingredient"]
                if ingredient in [
                    "Salami",
                    "Schnitzel",
                    "Leg Ham",
                    "Turkey",
                    "Meatball",
                    "Tuna",
                    "Grilled Chicken",
                    "Roast Beef",
                    "BBQ Pulled Pork",
                    "Veggie Pattie",
                ]:
                    meat.setFill(button["ingredient_colour"])
                elif ingredient in ["Old English", "Cheddar", "Mozzarella", "Swiss"]:
                    cheese.setFill(button["ingredient_colour"])
                elif ingredient in [
                    "Lettuce1",
                    "Tomato1",
                    "Onion1",
                    "Carrot1",
                    "Spinach1",
                    "Olive1",
                ]:
                    vegetable2.setFill(button["ingredient_colour"])
                elif ingredient in [
                    "Lettuce2",
                    "Tomato2",
                    "Onion2",
                    "Carrot2",
                    "Spinach2",
                    "Olive2",
                ]:
                    vegetable1.setFill(button["ingredient_colour"])
                elif ingredient in [
                    "Ketchup",
                    "Mayo",
                    "Chipotle",
                    "BBQ",
                    "Sweet Chilli",
                    "Ranch",
                    "Honey Mustard",
                    "Aioli",
                    "Hot Sauce",
                ]:
                    sauce.setFill(button["ingredient_colour"])
                elif ingredient in ["RESET"]:
                    meat.setFill(button["ingredient_colour"])
                    cheese.setFill(button["ingredient_colour"])
                    vegetable2.setFill(button["ingredient_colour"])
                    vegetable1.setFill(button["ingredient_colour"])
                    sauce.setFill(button["ingredient_colour"])
                elif ingredient in ["YES"]:
                    bread1.setFill(button["ingredient_colour"])
                    bread2.setFill(button["ingredient_colour"])
                elif ingredient in ["NO"]:
                    bread1.setFill(button["ingredient_colour"])
                    bread2.setFill(button["ingredient_colour"])


def draw_ingredient(
    insertion_point=Point(85, 320),
    ingredient_radius=11,
    active_radius=20,
    ingredient_colour="lightpink",
    lable_text="Leg Ham",
    label_text_offset=25,
    text_size=10,
):
    """Draws an ingredient button, ingredient circle and label text on the screen."""
    button = Circle(insertion_point, active_radius)
    button.setFill("pink")
    button.setOutline("pink")
    button.draw(win)
    BUTTON_LIST.append(
        {
            "insertion_point": insertion_point,
            "active_radius": active_radius,
            "ingredient": lable_text,
            "ingredient_colour": ingredient_colour,
        }
    )

    ingredient_graphic = Circle(insertion_point, ingredient_radius)
    ingredient_graphic.setFill(ingredient_colour)
    ingredient_graphic.draw(win)
    label_text = place_label_text(
        Point(insertion_point.getX(), insertion_point.getY() + label_text_offset),
        lable_text,
        size=text_size,
    )
    return button, ingredient_graphic, label_text


def place_label_text(insertion_pt, label, size=15, textcolor="teal", style="bold"):
    label_text = Text(insertion_pt, label)
    label_text.setSize(size)
    label_text.setStyle(style)
    label_text.setTextColor(textcolor)
    label_text.draw(win)
    return label_text


def make_rectangle(bottom_left_pt, top_right_pt, colour="navajowhite"):
    bread = Rectangle(bottom_left_pt, top_right_pt)
    bread.setFill(colour)
    bread.draw(win)
    return bread


def distance(p1, p2):
    return ((p1.getX() - p2.getX()) ** 2 + (p1.getY() - p2.getY()) ** 2) ** 0.5


def helppage(win):
    win.setBackground("lightcoral")
    helptitle = place_label_text(Point(375, 75), "Help Page", size=80, textcolor="pink")
    # Help Boxes
    whatisbox = make_rectangle(Point(50, 150), Point(250, 360), colour="pink")
    whatisboxtext = place_label_text(Point(150, 170), "What is this?", size=20)
    howtobox = make_rectangle(Point(275, 150), Point(600, 360), colour="pink")
    howtoboxtext = place_label_text(
        Point(440, 170), "How do you play this?", textcolor="teal"
    )
    isnttherebox = make_rectangle(Point(50, 375), Point(375, 525), colour="pink")
    isntthereboxtext = place_label_text(
        Point(215, 395), "The ingredient I wans isnt there!"
    )
    # What is this game Information text
    whatistext1 = place_label_text(
        Point(150, 200), "This is a game where", size=13, style="normal"
    )
    whatistext2 = place_label_text(
        Point(150, 220), "you can create your", size=13, style="normal"
    )
    whatistext3 = place_label_text(
        Point(150, 240), "own subway sandwich!", size=13, style="normal"
    )
    whatistext4 = place_label_text(
        Point(150, 260), "You can choose your", size=13, style="normal"
    )
    whatistext5 = place_label_text(
        Point(150, 280), "own ingredients that", size=13, style="normal"
    )
    whatistext6 = place_label_text(
        Point(150, 300), "you want to be", size=13, style="normal"
    )
    whatistext7 = place_label_text(
        Point(150, 320), "on your sandwich", size=13, style="normal"
    )
    # How to play Information text
    howtotext1 = place_label_text(
        Point(440, 200),
        "To use the simulation, you need to click on",
        size=13,
        style="normal",
    )
    howtotext2 = place_label_text(
        Point(440, 220),
        "the ingredients that you would like on",
        size=13,
        style="normal",
    )
    howtotext3 = place_label_text(
        Point(440, 240),
        "sandwich similar to the diagram on the right.",
        size=13,
        style="normal",
    )
    howtotext4 = Text(Point(440, 260), "If you would like your sandwich to be")
    howtotext4.setSize(13)
    howtotext4.setTextColor("teal")
    howtotext4.draw(win)
    howtotext5 = Text(Point(440, 280), "toasted, simply click the 'toasted' button.")
    howtotext5.setSize(13)
    howtotext5.setTextColor("teal")
    howtotext5.draw(win)
    howtotext6 = Text(Point(440, 300), "If you made a mistake in your preference,")
    howtotext6.setSize(13)
    howtotext6.setTextColor("teal")
    howtotext6.draw(win)
    howtotext7 = Text(Point(440, 320), "you can always click the 'reset' button")
    howtotext7.setSize(13)
    howtotext7.setTextColor("teal")
    howtotext7.draw(win)
    howtotext8 = Text(Point(440, 340), "to reset your sandwich to the original.")
    howtotext8.setSize(13)
    howtotext8.setTextColor("teal")
    howtotext8.draw(win)
    # My ingredient isnt there Information text
    isnttheretext1 = Text(Point(215, 425), "This simulation does not have every single")
    isnttheretext1.setSize(13)
    isnttheretext1.setTextColor("teal")
    isnttheretext1.draw(win)
    isnttheretext2 = Text(Point(215, 445), "ingredient that is offered at subway,")
    isnttheretext2.setSize(13)
    isnttheretext2.setTextColor("teal")
    isnttheretext2.draw(win)
    isnttheretext3 = Text(Point(215, 465), "but it contains the most popular")
    isnttheretext3.setSize(13)
    isnttheretext3.setTextColor("teal")
    isnttheretext3.draw(win)
    isnttheretext4 = Text(Point(215, 485), "ingredients that are offered at subway.")
    isnttheretext4.setSize(13)
    isnttheretext4.setTextColor("teal")
    isnttheretext4.draw(win)
    isnttheretext5 = Text(Point(215, 505), "We are very sorry in advance.")
    isnttheretext5.setSize(13)
    isnttheretext5.setTextColor("teal")
    isnttheretext5.draw(win)
    # Image
    try:
        referenceimage = Image(Point(800, 250), "Imageforinfo.png")
        referenceimage.draw(win)
    except:
        print("Couldn't find the image")
    # Arrow
    arrowline = Line(Point(600, 240), Point(675, 240))
    arrowline.setWidth(5)
    arrowline.draw(win)
    arrowtriangle = Polygon(Point(675, 220), Point(675, 260), Point(715, 240))
    arrowtriangle.setFill("black")
    arrowtriangle.draw(win)
    # Cursor
    cursorrectangle = Polygon(
        Point(745, 365), Point(753, 365), Point(755, 375), Point(746, 375)
    )
    cursorrectangle.setFill("white")
    cursorrectangle.draw(win)
    cursortriangle = Polygon(Point(740, 335), Point(735, 365), Point(760, 365))
    cursortriangle.setFill("white")
    cursortriangle.draw(win)
    # Tip Text
    tiptext1 = Text(Point(550, 400), "TIP:")
    tiptext1.setSize(30)
    tiptext1.setTextColor("Magenta")
    tiptext1.draw(win)
    tiptext2 = Text(Point(550, 450), "CLICK IN THE")
    tiptext2.setSize(25)
    tiptext2.setTextColor("Magenta")
    tiptext2.draw(win)
    tiptext3 = Text(Point(550, 500), "CENTER OF THE")
    tiptext3.setSize(25)
    tiptext3.setTextColor("Magenta")
    tiptext3.draw(win)
    tiptext4 = Text(Point(550, 550), "INGREDIENTS")
    tiptext4.setSize(25)
    tiptext4.setTextColor("Magenta")
    tiptext4.draw(win)
    # Back button
    backbutton = make_rectangle(Point(20, 20), Point(100, 80), colour="orange2")
    backtext = place_label_text(Point(60, 50), "BACK", size=17)

    while True:
        click_point = win.getMouse()
        x = click_point.getX()
        y = click_point.getY()
        if (x >= 20 and x <= 100) and (y >= 20 and y <= 80):
            helptitle.undraw()
            whatisbox.undraw()
            whatisboxtext.undraw()
            howtobox.undraw()
            howtoboxtext.undraw()
            isnttherebox.undraw()
            isntthereboxtext.undraw()
            whatistext1.undraw()
            whatistext2.undraw()
            whatistext3.undraw()
            whatistext4.undraw()
            whatistext5.undraw()
            whatistext6.undraw()
            whatistext7.undraw()
            howtotext1.undraw()
            howtotext2.undraw()
            howtotext3.undraw()
            howtotext4.undraw()
            howtotext5.undraw()
            howtotext6.undraw()
            howtotext7.undraw()
            howtotext8.undraw()
            isnttheretext1.undraw()
            isnttheretext2.undraw()
            isnttheretext3.undraw()
            isnttheretext4.undraw()
            isnttheretext5.undraw()
            referenceimage.undraw()
            arrowline.undraw()
            arrowtriangle.undraw()
            cursorrectangle.undraw()
            cursortriangle.undraw()
            tiptext1.undraw()
            tiptext2.undraw()
            tiptext3.undraw()
            tiptext4.undraw()
            backbutton.undraw()
            backtext.undraw()
            main_page(win)


def main():
    main_page(win)


main()
