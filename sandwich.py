# (I need help with making the help page be able to be pressed multiple times)
import random

from graphics import *

win = GraphWin("Make your own subway sandwich!", 950, 600)
win.setBackground("powderblue")

# Container for buttons
# When you make a new button, append it to this this list.
# Then later on, when you're checking for clicks, you can loop through this list
BUTTON_LIST = []


def main():
    # Title
    title = Text(Point(475, 30), "Make your own subway sandwich!")
    title.setSize(40)
    title.setStyle("bold")
    title.setTextColor("pink")
    title.draw(win)

    # Sandwich
    bread1 = make_bread(Point(300, 75), Point(700, 100), colour="navajowhite")
    bread2 = make_bread(Point(300, 205), Point(700, 230), colour="navajowhite")

    sauce = Rectangle(Point(285, 100), Point(715, 115))
    sauce.setFill("darkgray")
    sauce.draw(win)
    vegetable1 = Rectangle(Point(275, 115), Point(725, 140))
    vegetable1.setFill("darkgray")
    vegetable1.draw(win)
    vegetable2 = Rectangle(Point(265, 140), Point(735, 165))
    vegetable2.setFill("darkgray")
    vegetable2.draw(win)
    cheese = Rectangle(Point(300, 165), Point(700, 180))
    cheese.setFill("darkgray")
    cheese.draw(win)
    meat = Rectangle(Point(265, 180), Point(735, 205))
    meat.setFill("darkgray")
    meat.draw(win)

    # Ingredient boxes
    meatbox = Rectangle(Point(50, 260), Point(200, 580))
    meatbox.setFill("pink")
    meatbox.draw(win)

    cheesebox = Rectangle(Point(225, 260), Point(375, 440))
    cheesebox.setFill("pink")
    cheesebox.draw(win)

    vegetablebox1 = Rectangle(Point(400, 260), Point(550, 475))
    vegetablebox1.setFill("pink")
    vegetablebox1.draw(win)
    vegetablebox2 = Rectangle(Point(575, 260), Point(725, 475))
    vegetablebox2.setFill("pink")
    vegetablebox2.draw(win)
    meatboxtext = place_label_text(Point(125, 290), "Meat:")
    cheeseboxtext = place_label_text(Point(300, 290), "Cheese:")
    vegetablebox1text = place_label_text(Point(475, 290), "Vegetable 1:")
    vegetablebox2text = place_label_text(Point(650, 290), "Vegetable 2:")

    # Meat

    legham_button, legham, leghamtext = draw_ingredient(
        insertion_point=Point(85, 320),
        active_radius=25,
        ingredient_radius=11,
        ingredient_colour="lightpink",
        lable_text="Leg Ham",
        label_text_offset=25,
        text_size=10,
    )

    # schnitzel = Oval(Point(145, 309), Point(185, 335))
    schnitzel_button, schnitzel, schnitzeltext = draw_ingredient(
        insertion_point=Point(165, 320),
        ingredient_colour="chocolate3",
        lable_text="Schnitzel",
    )

    salami_button, salami, salamitext = draw_ingredient(
        insertion_point=Point(85, 375),
        ingredient_colour="firebrick1",
        lable_text="Salami",
    )

    # turkey = Oval(Point(145, 360), Point(185, 385))
    turkey_button, turkey, turkeytext = draw_ingredient(
        insertion_point=Point(165, 375),
        ingredient_colour="cornsilk",
        lable_text="Turkey",
    )

    tuna = Rectangle(Point(65, 420), Point(105, 440))
    tuna.setFill("burlywood2")
    tuna.draw(win)
    tunatext = place_label_text(Point(85, 455), "Tuna", size=10)

    meatball = Circle(Point(165, 430), 11)
    meatball.setFill("brown3")
    meatball.draw(win)
    meatballtext = place_label_text(Point(165, 456), "Meatball", size=10)

    grilledchicken = Oval(Point(65, 470), Point(105, 495))
    grilledchicken.setFill("bisque1")
    grilledchicken.draw(win)
    grilledchickentext = place_label_text(Point(90, 510), "Grilled Chicken", size=8)

    roastbeef = Oval(Point(145, 470), Point(185, 495))
    roastbeef.setFill("antiquewhite4")
    roastbeef.draw(win)
    roastbeeftext = place_label_text(Point(170, 510), "Roast Beef", size=8)

    bbqpulledpork = Rectangle(Point(65, 530), Point(105, 540))
    bbqpulledpork.setFill("burlywood4")
    bbqpulledpork.draw(win)
    bbqpulledporktext = place_label_text(Point(90, 555), "BBQ Pulled Pork", size=7)

    veggiepattie = Rectangle(Point(145, 525), Point(190, 545))
    veggiepattie.setFill("sandybrown")
    veggiepattie.draw(win)
    veggiepattietext = place_label_text(Point(168, 555), "Veggie Pattie", size=7)

    # Cheese
    oldenglish = Polygon(Point(265, 315), Point(250, 340), Point(280, 340))
    oldenglish.setFill("gold")
    oldenglish.draw(win)
    oldenglishtext = place_label_text(Point(265, 360), "Old English", size=10)

    cheddar = Polygon(Point(335, 315), Point(320, 340), Point(350, 340))
    cheddar.setFill("oldlace")
    cheddar.draw(win)
    cheddartext = place_label_text(Point(335, 360), "Cheddar", size=10)

    mozzarella = Rectangle(Point(250, 380), Point(280, 400))
    mozzarella.setFill("palegoldenrod")
    mozzarella.draw(win)
    mozzarellatext = place_label_text(Point(265, 415), "Mozzarella", size=10)

    swiss = Polygon(Point(335, 375), Point(320, 400), Point(350, 400))
    swiss.setFill("lightgoldenrodyellow")
    swiss.draw(win)
    swisstext = place_label_text(Point(335, 415), "Swiss", size=10)

    # First vegetable
    lettuce1 = Rectangle(Point(410, 315), Point(450, 330))
    lettuce1.setFill("DarkOliveGreen1")
    lettuce1.draw(win)
    lettuce1text = place_label_text(Point(430, 345), "Lettuce", size=10)

    tomato1 = Circle(Point(510, 325), 11)
    tomato1.setFill("tomato")
    tomato1.draw(win)
    tomato1text = place_label_text(Point(510, 346), "Tomato", size=10)

    onion1 = Circle(Point(430, 375), 11)
    onion1.setFill("plum1")
    onion1.draw(win)
    onion1text = place_label_text(Point(430, 395), "Onion", size=10)

    carrot1 = Rectangle(Point(490, 365), Point(535, 380))
    carrot1.setFill("orange")
    carrot1.draw(win)
    carrot1text = place_label_text(Point(510, 395), "Carrot", size=10)

    spinach1 = Oval(Point(415, 415), Point(450, 440))
    spinach1.setFill("darkgreen")
    spinach1.draw(win)
    spinach1text = place_label_text(Point(430, 450), "Spinach", size=10)

    olive1 = Circle(Point(510, 429), 9)
    olive1.setFill("grey13")
    olive1.draw(win)
    olive1text = place_label_text(Point(510, 450), "Olive", size=10)

    # Second Vegetable
    lettuce2 = Rectangle(Point(585, 315), Point(625, 330))
    lettuce2.setFill("DarkOliveGreen1")
    lettuce2.draw(win)
    lettuce2text = place_label_text(Point(605, 345), "Lettuce", size=10)

    tomato2 = Circle(Point(685, 325), 11)
    tomato2.setFill("tomato")
    tomato2.draw(win)
    tomato2text = place_label_text(Point(685, 345), "Tomato", size=10)
    onion2 = Circle(Point(605, 375), 11)
    onion2.setFill("plum1")
    onion2.draw(win)
    onion2text = place_label_text(Point(605, 395), "Onion", size=10)
    carrot2 = Rectangle(Point(665, 365), Point(710, 380))
    carrot2.setFill("orange")
    carrot2.draw(win)
    carrot2text = place_label_text(Point(685, 395), "Carrot", size=10)
    spinach2 = Oval(Point(590, 415), Point(625, 440))
    spinach2.setFill("darkgreen")
    spinach2.draw(win)
    spinach2text = place_label_text(Point(605, 450), "Spinach", size=10)
    olive2 = Circle(Point(685, 429), 9)
    olive2.setFill("grey13")
    olive2.draw(win)
    olive2text = place_label_text(Point(685, 450), "Olive", size=10)
    # Sauce
    saucebox = Rectangle(Point(750, 260), Point(900, 570))
    saucebox.setFill("pink")
    saucebox.draw(win)
    sauceboxtext = place_label_text(Point(825, 290), "Sauce:")
    ketchup, ketchup_text = draw_sauce_menu_item(
        insertion_pt=Point(785, 325), size=11, colour="orangered", label_text="Ketchup"
    )
    mayo, mayo_text = draw_sauce_menu_item(
        insertion_pt=Point(865, 325), size=11, colour="cornsilk", label_text="Mayo"
    )
    # This ^^^ can be replaced by just this vvv
    # mayo = Circle(Point(865, 325), 12)
    # mayo.setFill("cornsilk")
    # mayo.draw(win)
    # mayotext = place_label_text(Point(865, 345), "Mayo", size=10)
    chipotle = Circle(Point(785, 375), 12)
    chipotle.setFill("sandybrown")
    chipotle.draw(win)
    chipotletext = place_label_text(Point(785, 395), "Chipotle", size=10)

    bbq = Circle(Point(865, 374), 12)
    bbq.setFill("orangered4")
    bbq.draw(win)
    bbqtext = place_label_text(Point(865, 395), "BBQ", size=9)

    sweetchilli = Circle(Point(785, 425), 12)
    sweetchilli.setFill("orangered3")
    sweetchilli.draw(win)
    sweetchillitext = place_label_text(Point(785, 445), "Sweet Chilli", size=9)

    ranch = Circle(Point(865, 425), 12)
    ranch.setFill("ghostwhite")
    ranch.draw(win)
    ranchtext = place_label_text(Point(865, 445), "Ranch", size=9)

    honeymustard = Circle(Point(785, 475), 12)
    honeymustard.setFill("gold2")
    honeymustard.draw(win)
    honeymustardtext = place_label_text(Point(790, 495), "Honey Mustard", size=8)

    aioli = Circle(Point(865, 475), 12)
    aioli.setFill("wheat1")
    aioli.draw(win)
    aiolitext = place_label_text(Point(865, 495), "Aioli", size=9)
    hotsauce = Circle(Point(830, 530), 12)
    hotsauce.setFill("orangered2")
    hotsauce.draw(win)
    hotsaucetext = place_label_text(Point(830, 555), "Hot Sauce", size=9)
    # Information
    helpbox = Rectangle(Point(800, 100), Point(870, 150))
    helpbox.setFill("orange2")
    helpbox.draw(win)
    helptext = Text(Point(835, 125), "HELP")
    helptext.setSize(17)
    helptext.setStyle("bold")
    helptext.setTextColor("teal")
    helptext.draw(win)
    # Toasted
    toastedtext = Text(Point(90, 125), "Toasted?")
    toastedtext.setSize(17)
    toastedtext.setStyle("bold")
    toastedtext.setTextColor("teal")
    toastedtext.draw(win)

    yesbox = Rectangle(Point(20, 150), Point(80, 200))
    yesbox.setFill("lawngreen")
    yesbox.draw(win)
    yestext = Text(Point(50, 175), "YES")
    yestext.setSize(17)
    yestext.setStyle("bold")
    yestext.setTextColor("teal")
    yestext.draw(win)

    nobox = Rectangle(Point(100, 150), Point(160, 200))
    nobox.setFill("red")
    nobox.draw(win)
    notext = Text(Point(130, 175), "NO")
    notext.setSize(17)
    notext.setStyle("bold")
    notext.setTextColor("teal")
    notext.draw(win)

    # Reset
    resetbox = Rectangle(Point(790, 175), Point(880, 225))
    resetbox.setFill("magenta")
    resetbox.draw(win)
    resettext = Text(Point(835, 200), "RESET")
    resettext.setSize(17)
    resettext.setStyle("bold")
    resettext.setTextColor("teal")
    resettext.draw(win)
    resetbox.getCenter()

    while True:
        click_point = win.getMouse()
        print(click_point)
        for button in BUTTON_LIST:
            if (
                distance(button["insertion_point"], click_point)
                < button["active_radius"]
            ):
                print(f"Clicked on {button['ingredient']}")
                ingredient = button["ingredient"]
                if ingredient in ["Salami", "Schnitzel", "Leg Ham", "Turkey"]:
                    meat.setFill(button["ingredient_colour"])

    # if 800 < click_point.getX() < 870 and 100 < click_point.getY() < 150:
    #     help1 = GraphWin("Help", 950, 600)
    #     help1.setBackground("powderblue")
    # # Title
    # helptitle = Text(Point(350, 50), "Help Page")
    # helptitle.setSize(70)
    # helptitle.setStyle("bold")
    # helptitle.setTextColor("pink")
    # helptitle.draw(help1)
    # # Help Boxes
    # whatisbox = Rectangle(Point(50, 150), Point(250, 360))
    # whatisbox.setFill("pink")
    # whatisbox.draw(help1)
    # whatisboxtext = Text(Point(150, 170), "What is this?")
    # whatisboxtext.setSize(20)
    # whatisboxtext.setStyle("bold")
    # whatisboxtext.setTextColor("teal")
    # whatisboxtext.draw(help1)
    # howtobox = Rectangle(Point(275, 150), Point(600, 360))
    # howtobox.setFill("pink")
    # howtobox.draw(help1)
    # howtoboxtext = Text(Point(440, 170), "How do you play this?")
    # howtoboxtext.setSize(20)
    # howtoboxtext.setStyle("bold")
    # howtoboxtext.setTextColor("teal")
    # howtoboxtext.draw(help1)
    # isnttherebox = Rectangle(Point(50, 375), Point(375, 525))
    # isnttherebox.setFill("pink")
    # isnttherebox.draw(help1)
    # isntthereboxtext = Text(Point(215, 395), "The ingredient I want isnt there!")
    # isntthereboxtext.setSize(15)
    # isntthereboxtext.setStyle("bold")
    # isntthereboxtext.setTextColor("teal")
    # isntthereboxtext.draw(help1)
    # # What is this game Information text
    # whatistext1 = Text(Point(150, 200), "This is a game where")
    # whatistext1.setSize(13)
    # whatistext1.setTextColor("teal")
    # whatistext1.draw(help1)
    # whatistext2 = Text(Point(150, 220), "you can create your")
    # whatistext2.setSize(13)
    # whatistext2.setTextColor("teal")
    # whatistext2.draw(help1)
    # whatistext3 = Text(Point(150, 240), "own subway sandwich!")
    # whatistext3.setSize(13)
    # whatistext3.setTextColor("teal")
    # whatistext3.draw(help1)
    # whatistext4 = Text(Point(150, 260), "You can choose your")
    # whatistext4.setSize(13)
    # whatistext4.setTextColor("teal")
    # whatistext4.draw(help1)
    # whatistext5 = Text(Point(150, 280), "own ingredients that")
    # whatistext5.setSize(13)
    # whatistext5.setTextColor("teal")
    # whatistext5.draw(help1)
    # whatistext6 = Text(Point(150, 300), "you want to be")
    # whatistext6.setSize(13)
    # whatistext6.setTextColor("teal")
    # whatistext6.draw(help1)
    # whatistext7 = Text(Point(150, 320), "on your sandwich")
    # whatistext7.setSize(13)
    # whatistext7.setTextColor("teal")
    # whatistext7.draw(help1)
    # # How to play Information text
    # howtotext1 = Text(Point(440, 200), "To use the simulation, you need to click on")
    # howtotext1.setSize(13)
    # howtotext1.setTextColor("teal")
    # howtotext1.draw(help1)
    # howtotext2 = Text(Point(440, 220), "the ingredients that you would like on your")
    # howtotext2.setSize(13)
    # howtotext2.setTextColor("teal")
    # howtotext2.draw(help1)
    # howtotext3 = Text(Point(440, 240), "sandwich similar to the diagram on the right.")
    # howtotext3.setSize(13)
    # howtotext3.setTextColor("teal")
    # howtotext3.draw(help1)
    # howtotext4 = Text(Point(440, 260), "If you would like your sandwich to be")
    # howtotext4.setSize(13)
    # howtotext4.setTextColor("teal")
    # howtotext4.draw(help1)
    # howtotext5 = Text(Point(440, 280), "toasted, simply click the 'toasted' button.")
    # howtotext5.setSize(13)
    # howtotext5.setTextColor("teal")
    # howtotext5.draw(help1)
    # howtotext6 = Text(Point(440, 300), "If you made a mistake in your preference,")
    # howtotext6.setSize(13)
    # howtotext6.setTextColor("teal")
    # howtotext6.draw(help1)
    # howtotext7 = Text(Point(440, 320), "you can always click the 'reset' button")
    # howtotext7.setSize(13)
    # howtotext7.setTextColor("teal")
    # howtotext7.draw(help1)
    # howtotext7 = Text(Point(440, 340), "to reset your sandwich to the original.")
    # howtotext7.setSize(13)
    # howtotext7.setTextColor("teal")
    # howtotext7.draw(help1)
    # # My ingredient isnt there Information text
    # isnttheretext1 = Text(Point(215, 425), "This simulation does not have every single")
    # isnttheretext1.setSize(13)
    # isnttheretext1.setTextColor("teal")
    # isnttheretext1.draw(help1)
    # isnttheretext2 = Text(Point(215, 445), "ingredient that is offered at subway,")
    # isnttheretext2.setSize(13)
    # isnttheretext2.setTextColor("teal")
    # isnttheretext2.draw(help1)
    # isnttheretext3 = Text(Point(215, 465), "but it contains the most popular")
    # isnttheretext3.setSize(13)
    # isnttheretext3.setTextColor("teal")
    # isnttheretext3.draw(help1)
    # isnttheretext4 = Text(Point(215, 485), "ingredients that are offered at subway.")
    # isnttheretext4.setSize(13)
    # isnttheretext4.setTextColor("teal")
    # isnttheretext4.draw(help1)
    # isnttheretext5 = Text(Point(215, 505), "We are very sorry in advance.")
    # isnttheretext5.setSize(13)
    # isnttheretext5.setTextColor("teal")
    # isnttheretext5.draw(help1)
    # # Image
    # referenceimage = Image(Point(800, 250), "Imageforinfo.png")
    # referenceimage.draw(help1)
    # # Arrow
    # arrowline = Line(Point(600, 240), Point(675, 240))
    # arrowline.setWidth(5)
    # arrowline.draw(help1)
    # arrowtriangle = Polygon(Point(675, 220), Point(675, 260), Point(715, 240))
    # arrowtriangle.setFill("black")
    # arrowtriangle.draw(help1)
    # # Cursor
    # cursorrectangle = Polygon(
    #     Point(745, 365), Point(753, 365), Point(755, 375), Point(746, 375)
    # )
    # cursorrectangle.setFill("white")
    # cursorrectangle.draw(help1)

    # cursortriangle = Polygon(Point(740, 335), Point(735, 365), Point(760, 365))
    # cursortriangle.setFill("white")
    # cursortriangle.draw(help1)
    # # Tip Text
    # tiptext1 = Text(Point(550, 400), "TIP:")
    # tiptext1.setSize(30)
    # tiptext1.setTextColor("Magenta")
    # tiptext1.draw(help1)
    # tiptext2 = Text(Point(550, 450), "CLICK IN THE")
    # tiptext2.setSize(25)
    # tiptext2.setTextColor("Magenta")
    # tiptext2.draw(help1)
    # tiptext3 = Text(Point(550, 500), "CENTER OF THE")
    # tiptext3.setSize(25)
    # tiptext3.setTextColor("Magenta")
    # tiptext3.draw(help1)
    # tiptext4 = Text(Point(550, 550), "INGREDIENTS")
    # tiptext4.setSize(25)
    # tiptext4.setTextColor("Magenta")
    # tiptext4.draw(help1)


def draw_ingredient(
    insertion_point=Point(85, 320),
    active_radius=25,
    ingredient_radius=11,
    ingredient_colour="lightpink",
    lable_text="Leg Ham",
    label_text_offset=25,
    text_size=10,
):
    """Draws an ingredient button, ingredient circle and label text on the screen."""
    button = Circle(insertion_point, active_radius)
    button.setFill("pink")
    button.setOutline("lightpink")
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


def draw_sauce_menu_item(
    insertion_pt=Point(785, 325), size=11, colour="orangered", label_text="Ketchup"
):
    spot = Circle(insertion_pt, size)
    spot.setFill(colour)
    spot.draw(win)
    label_text = place_label_text(
        Point(insertion_pt.x, insertion_pt.y + 20), label_text, size=10
    )
    return spot, label_text


def place_label_text(insertion_pt, label, size=15):
    label_text = Text(insertion_pt, label)
    label_text.setSize(size)
    label_text.setStyle("bold")
    label_text.setTextColor("teal")
    label_text.draw(win)
    return label_text


def make_bread(bottom_left_pt, top_right_pt, colour="navajowhite"):
    bread = Rectangle(bottom_left_pt, top_right_pt)
    bread.setFill(colour)
    bread.draw(win)
    return bread


def distance(p1, p2):
    return ((p1.getX() - p2.getX()) ** 2 + (p1.getY() - p2.getY()) ** 2) ** 0.5


main()
