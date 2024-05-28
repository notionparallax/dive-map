# 📌 Making a dive map of Gordon's bay, a WIP 🗺

As part of my [divemaster course](https://www.prodive.com.au/Sydney+-+Alexandria/Divemaster+/Divemaster+Orientation+/1124), I need to make a map of a dive site. I'm doing Gordon's bay. It's a marine reserve, and it's very pretty. It also has a [scuba club](https://www.gordonsbayscubadiving.com/), and the club maintains an underwater trail around the bay that divers can follow without too much worry of getting lost.

Oddly, there's no good map of Gordon's that I've found. There are a couple of maps ([a](https://www.gordonsbayscubadiving.com/trail.html), [b](https://www.viz.net.au/maps-of-shore-dive-sites/gordons-bay)) that show the trail, the Google Maps satellite map, and another satellite map from [Michael McFadyen's website](https://www.michaelmcfadyenscuba.info/viewpage.php?page_id=282).

<figure>

![Several maps of Gordon's bay, overlaid on each other](docs/gordons_early_stage.PNG)

<figcaption>Several maps of Gordon's bay, overlaid on each other.</figcaption>

</figure>

## What can I do better?

The maps above are very sparse, so making one a bit better is going to be quite easy, but can I make one a lot better? Can I approach [this](https://www.viz.net.au/maps-of-shore-dive-sites/bare-island) quality?

### GPS

Following [Marco Bordieri](https://www.viz.net.au/do-it-yourself/a-surfaceable-gps)'s lead, I've bought myself a [waterproof box](https://www.anacondastores.com/fishing/fishing-storage/tackle-boxes/plano-guide-series-1450-waterproof-case/90038539) to put my phone in. I'm going to make a _very_ shoddy surface bouy out of a milk crate, a body board, and a dive flag.

![](https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExdnU1NXdmZHlkdDV3Y2Nhcjh2dmpmaDFlZnp2OWE1NmRqMWlwcTMyZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3xRDrsbA7is1ot0EFy/giphy-downsized-large.gif)

https://youtu.be/xZAZsOZbFWw?si=KpQPosB-lPe8R0lN

The plan now is to drag that around the trail, and the other underwater features, to get a map of where I've been. Then merge the resulting `.gpx` file with the data from my watch (somehow) to get depths and important times.

### String survey

I've marked a builders' string at 2m intervals, so I'll lay down the line, and take depths, manually in my wet notes. This will give some sense of whether or not the contours from the map are right or not.

### Loads of photos

Taking a tonne of pictures and videos will give me a sense of what to draw.

### Draw the rest of the fucking owl

![Instructions for drawing an owl](docs/owl.PNG)

### GPS testing

I've started testing what the GPS tracker gives me. The `.gpx` file in this repo is me walking around the block at work.

![a folium map of the pitt/george st block with a red line showing the walking path I took.](docs/bvn_block_map.PNG)

This isn't perfect, e.g. I didn't cross the road on the right hand side, but I'm hoping that's down to map inaccuracy, not GPS drift. Hopefully, given that there's a good view of the sky from the ocean, and the data will all match up with itself.

The stack for this is:

1. A [GPS Logger](https://play.google.com/store/apps/details?id=eu.basicairdata.graziano.gpslogger&hl=en&gl=US) app. This one works well, exports easily to google drive, and doesn't chew through my battery.
2. A [Sunnto D5](https://www.suunto.com/en-au/Products/dive-computers-and-instruments/suunto-d5/suunto-d5-white/) computer. Works fine, exports to a `.fit` file from the phone.
3. A [GoPro 12](https://gopro.com/en/au/shop/cameras/hero12-black/CHDHX-121-master.html). These photos are useful because it means I don't need to get the wet notes out, I can just take photos and then see where the photos are on the GPS track. The 12 doesn't actually have GPS, but that doesn't really matter because it doesn't work underwater anyway. You could use any camera at all, we're just interested in the EXIF data.
4. A bit of python in a GitHub Codespace. I can't install packages on my work computer, but I can do everything I need to in a remote machine, for free.

Something that's interesting is that I didn't need to install anything on my laptop, or run any code locally\*, I was able to export all the data using my phone and Google Drive.

- That's not quite true, I did need to [extract the EXIF] data, but that only used libraries that are in the standard work image.

### First and second GPS dive

Tali and I went for a swim around the chain on 9/3/24 and dragged the GPS float (photos of that coming). I left the GPS running the whole morning and it was actually completely fine, no overheating or battery issues.

![Me, touching a marker on a barrel](docs/GOPR0211.JPG)

I swam the float around, and touched my computer hand to the base of each numbered marker, and intermediary buoy, and while my hand was there, [Tali took a photo](https://gopro.com/v/WlwGaV9nvZ5RO). The timestamps from the EXIF data tell me when I was at a marker. (Also, I know my tank trim is horrible. I'm going to fix that.)

We did two dives, one around the chain, and one following the sand line of the boulder garden.

You can see how the data is processed in `mapper.py`, it gives an output like this:

![an xy plot of the paths on a pain axis](docs/plain_graph.png)

The red is the first (chain) dive, and the green is the second (boulder garden) dive. The blue sections are where the photos were taken.

I overlaid the tracks onto a folium map, and then overlaid _that_ into the existing maps I've been collecting. The interesting thing is that the GPS trail is not only a different size, it's a substantially different shape.

![the overlaid maps from above, but with the GPS tracks as well](docs/gordons_with_gps_tracks.PNG)

The first map was drawn in 1990 by Jöelle Devis, and it's really good. Odd that it's so hard to find on the internet, and odder that it hasn't been updated. I found it because the inset map is republished on [Michael McFadyen's website](https://www.michaelmcfadyenscuba.info/viewpage.php?page_id=282). My guess is that this map is drawn by dead reckoning, using distances and headings. It's also possible that sections of the chain have moved over the last 34 years. There is a whole load of interesting trail-history, as well as this full map [on the Gordon's bay scuba club's _club history_ page](https://www.gordonsbayscubadiving.com/clubHistory.html).

![a hand drawn map of the chain trail with a zoomed out context map as well](docs/gordons_map_1990.png)

There is going to be some degree of inaccuracy in the GPS track, and I need to calculate that once I get the depth data. I can assume that the float line is the edge of a cone, probably less than 80° at the point. So there will be more error possible at depth. I should be able to draw those circles.

#### Some more progress (10/3/24)

![a map showing coloured dots for depth along the GPS trail, and the position of the photos is labeled](docs/map_of_depth_and_photos.png)

This shows the position of the photos and the depths along the trail.

There's a [zoomable map that shows the path from the dives here](https://notionparallax.github.io/dive-map/gordons_map).

[![a bright line tracing the chain overlaid onto a satellite photo of Gordon's bay](/docs/interactive_thumbnail.PNG)](https://notionparallax.github.io/dive-map/gordons_map)

I don't have data for a few of the markers. I'm not sure if the camera just didn't go off, or the marker is buried in the sand, or what. I also need to add in the intermediate buoys because I don't think the runs are straight between the numbered markers.

![](docs/marker_graph.png)

This shows the numbered markers that I have waypoints for, but the missing points don't seem to be at the obvious corners. More will be revealed when I do another dive, and when I've found a way to pinpoint the intermediate buoys.

There's quite a lot going on in that graph now!

- The orange Os are the numbered markers They are labelled with their marker number, and the file name of the photo
- The ![](https://matplotlib.org/stable/_images/m08.png) is an un-numbered marker. (I've got a plan to map these out properly, but it's going to be a fair bit of work.) They are labelled with the file name of the photo
- The rainbow line is the path we swam around the chain. It's coloured by depth, and that depth is shown in the colour bar on the right
- The dashed circles around the numbered markers show tolerance. This is where the point _could_ be if the wind or current etc. was pushing the float around. They assume that the marker is the tip of a downward facing cone, and that cone has a tip angle of 70°. The circle is where the cone intersects the surface.
- The coloured blocks in the background show the ground condition. Each photo has a ground condition, and it's using a [voronoi diagram](https://en.wikipedia.org/wiki/Voronoi_diagram) to assume that condition until another point's influence takes over. This is going to need a _lot_ more swimming around to get it to be useful, but the infrastructure is there for that data when it comes.

  | Photo                  | Metadata                                                                                                                                                                                                                                                                                                                                              |
  | ---------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
  | ![](docs/GOPR0193.JPG) | This is the data entry in `photo_meta.py`: <pre>{<br> "dt": datetime.datetime(2024, 3, 8, 10, 6, 29),<br> "filename": "GOPR0193.JPG",<br> "marker_type": "intermediate",<br> "marker_number": "",<br> "bottom_condition": "kelp",<br> }</pre> I don't know if keeping going with this method is the best idea, or if I should just use a spreadsheet. |

### Third and fourth GPS dive

Shuwen and I dived on Saturday the 23rd of March, and did a couple of things:

1. Outline the edge of the deep sandy part next to the wall. If you're heading out into the ocean, the wall is on your left, and everything up to the wall is kelpy rock, and to your right is sand. There's not much to see down here, but I've got an edge now.
1. Swam across to the other side. Not a huge amount to see, but it's shallow, so the sun beams were very pretty and sparkly. We saw 3 separate wobbegongs sleeping under rocks. This was useful because it gives a depth profile for the whole width of the bay, but more pragmatically, it shows that the scale is right. There's a bit at the turn around where we swim around a rock that sticks out of the water, so when the trace is drawn over the photo, that part matches up.

I got a lot more bottom condition data points. I've been struggling with the voronoi, but it's semi working and it shows that I'm going to need way more data if I'm going to take that approach to mapping! I think the old fashioned approach is probably the way to go to some extent.

### Dive day 3

Long dive, trying to do some zigzags over the west side, past the chain, that I'm provisionally calling the golf course. Turns out that I'm terrible at holding a compass bearing, so it was just a big loop.

### Dive day 4

An even longer dive (my longest so far at 1:40) trying to find the bommie. I didn't put my compass on, and I discovered that underwater I can't calibrate my watch compass (Thanks Sunnto, that's very helpful). But I did have a 100m line. So I swam in a "straight line due south" while reeling out the line. I ended up facing north west it turns out, but then I followed the arc of the line and found the bommie anyway, and got some good depth data for the sandy bit out in the ocean.

The bommie was surgey, so I didn't spend long there. I tied off the line, and had a little swim. When I got back there was a stonefish camped out on the spool at the tie off; that was fun to move, those guys really don't care.

Because I didn't do a full circumnavigation of the bommie, I was a bit concerned that it's be a mystery what it looked like. Then I had a bit of a breakthrough. If I sighted through the part that breaches the surface, I can work out an intersection:

![](docs\eyeballing_small.PNG)

That's given me enough context to be able to interpret the aerial photos enough to guess at the bommie's shape and extent.

---

Things to do on the next dives:

- [ ] Swim around the bay with the gps, to get a perimeter. Probably as a snorkle and then I can sketch/photograph some features for the actual map drawing part
- [ ] Visit the bommie drawn off marker 14 on the 1990 map, and swim a perimeter on it
- [x] try to find marker 2. Marker 3 doesn't have a number on it, as far as I can tell, so maybe 2 isn't there any more? Just needs a bit of searching.
- [ ] Map the intermediate markers more carefully
- [ ] Get some more perimeters of kelp beds etc.
- [ ] Visit the cave at 12 (in 1990 numbers)
- [ ] draw the wall, so that I can draw it onto the map in a useful way
- [ ] do some zigzags over the wall to get better defined contours over the top of the wall

Things to do the the map:

- [ ] Work out the numbering. When did there become 25 points? This might be a question for the scuba club?
- [x] add the same shortcut arrows and headings, as a homage to the 1990 map
- [x] add a scale bar and north arrow
- [x] Import the map as an svg instead of a png
- [ ] Actually draw my map!
- [x] Make tire etc have shorter arrows
- [x] Hide intermediate markers

display todos (things to do before this goes to illustrator)

- [x] change swim traces from dots to polylines
- [x] remove intermediate photo labels
- [ ] turn off axis ticks and tick labels
- [ ] make sure the rest of the bottom condition markers are plotting (potentially fo an n^2 loop to check for inclusion so colour the cells properly?)
- [ ] check that `plt.rcParams['svg.fonttype'] = 'none'` is actually outputting text not curves

# WIP map

![](docs\Gordons_map_wip.png)

Some things to consider:

- Colours are there for my working brain, it'll simplify to one colour for the finished map
- There will only be one background image on the finished one. These are there for me to turn on and off so I can see how it relates to other maps
- (_fixed by changing interpolation to linear_)The contour lines are super chaotic in the areas without much depth data. More depth measurements will calm that down.
- The bommie is a total mystery
- It's 1:1000 at A2, but that's not a practical size to have at a dive site, so it's 1:2000 at A3 for now
- The chain length is currently 490, that doesn't visit #2 or #4, and it doesn't go back via 3, 2 and 1, which should bring it up to somewhere near Jöelle Devis's measured distance of 616m.
- I have to submit this map at some point, but there's still a lot that I can do to keep adding to this, so I'm going to keep going even after I've submitted it.
- I still don't know what kind of seaweed I'm marking up as _low_, I need a seaweed expert.
- There's a higher res output [here](docs\Gordons_map_wip@2x.png). Probably still not print quality though.
