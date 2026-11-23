"""Build the Nassau County town pages under areas-we-serve/.

One shot generator (Nov 2026). It copies the head, nav, styles and footer from
areas-we-serve/huntington.html and writes one page per town from the TOWNS data
below. Hand edits to the generated pages will be overwritten if this is rerun,
so edit the TOWNS data here instead. This script does not touch any other page.
"""
import html, json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parents[1]
TEMPLATE = (ROOT / "areas-we-serve/huntington.html").read_text()
BASE = "https://homecoregc.com"
LICENSE = "Nassau County Home Improvement License 205185"

TOWN_GRID_CSS = """    .town-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 26px 40px; }
    .town-grid h3 { color: var(--navy); font-size: 1.1rem; margin-bottom: 8px; }
    .town-grid p { line-height: 1.7; font-size: 0.95rem; }
    .town-grid a.more { color: var(--accent); font-weight: 700; font-size: 0.9rem; display: inline-block; margin-top: 8px; }
    @media (max-width: 700px) { .town-grid { grid-template-columns: 1fr; } }
"""

NAMES = {
    "garden-city": "Garden City", "rockville-centre": "Rockville Centre", "mineola": "Mineola",
    "westbury": "Westbury", "manhasset": "Manhasset", "massapequa": "Massapequa",
    "wantagh": "Wantagh", "oyster-bay": "Oyster Bay", "port-washington": "Port Washington",
    "great-neck": "Great Neck", "cold-spring-harbor": "Cold Spring Harbor",
}

def img(path, w, h, label, text):
    stem = path.rsplit(".", 1)[0]
    alt = html.escape(f"{label}: {text}", quote=True)
    return (f'<div class="stage"><figure><img src="{path}" alt="{alt}" width="{w}" height="{h}" loading="lazy" decoding="async" '
            f'srcset="{stem}-640w.webp 640w, {path} {w}w" sizes="(max-width: 700px) 100vw, 530px">'
            f'<figcaption><strong>{label}</strong>{text}</figcaption></figure></div>')

CH = "/images/projects/progress-stories/custom-home-1/"
BA = "/images/projects/progress-stories/bathroom-1/"

TOWNS = [
 dict(
  slug="garden-city", name="Garden City", short="Garden City",
  title="Contractor in Garden City, NY | Custom Homes, Kitchens &amp; Baths | HomeCore Construction",
  desc="HomeCore Construction is building a custom home and finished a master bathroom in Garden City. Kitchens, baths, additions and rebuilds for Garden City homes.",
  og=BASE + CH + "65-where-it-stands.jpg",
  hero="A custom home rebuild underway and a finished master bathroom, right here in the Village of Garden City.",
  h2="Building and Remodeling in Garden City",
  intro=[
   'Garden City was founded in 1869 by Alexander Turney Stewart as one of the first planned communities in the country, and it shows in the housing: brick and stucco Tudors, center hall colonials, shingled Dutch colonials and Capes on tree lined streets, many of them close to a century old. HomeCore Construction works on exactly these houses, from <a href="/kitchen-remodeling">kitchens</a> and <a href="/bathroom-remodeling">primary baths</a> to <a href="/home-additions">rear additions</a> and full <a href="/custom-homes">custom home rebuilds</a>.',
   'Older Garden City homes reward careful work. Plaster walls, original trim and small period baths are common, and the best remodels keep the character of the house while bringing the kitchen, baths and mechanicals up to date. Our cabinetry, vanities and trim are built in our own <a href="/custom-millwork">Long Island millwork shop</a>, so new work can be matched to what is already in the house.',
  ],
  jobs=[
   dict(eyebrow="In Progress", h2="A Custom Home Rebuild in Garden City",
        sub="A full rebuild with a rear addition: steel, framing, shingle siding and a stone veneer front porch with bluestone steps.",
        imgs=[img(CH+"65-where-it-stands.webp",1400,1050,"Where it stands","The front of the house with gray shingle siding, a stone veneer porch and new bluestone steps."),
              img(CH+"64-back-of-the-house-sided.webp",1400,1050,"Back of the house","The rear addition fully sided in gray shingles, with French doors and new windows."),
              img(CH+"57-stone-climbing-the-corner.webp",1050,1400,"Stone veneer","Masons setting stone veneer up the corner of the house from staging.")],
        links=[("/projects/progress-stories/custom-home-1","Follow the Build"),("/projects/projects-in-progress","Projects in Progress")]),
   dict(eyebrow="Finished", h2="A Finished Master Bathroom in Garden City",
        sub="A gut remodel with a frameless glass shower, a double vanity under arched mirrors and tile from floor to ceiling.",
        imgs=[img(BA+"37-double-vanity-under-arched-mirrors.webp",1400,1050,"Double vanity","A gray double vanity under a pair of arched mirrors."),
              img(BA+"42-frameless-glass-shower.webp",1050,1400,"Glass shower","The walk in shower behind frameless glass."),
              img(BA+"44-the-finished-master-bath.webp",1050,1400,"Finished","The finished master bath, ready for the homeowners.")],
        links=[("/projects/progress-stories/bathroom-1","See the Bath Story"),("/projects/past-projects","Past Projects")]),
  ],
  types=[("Custom home rebuilds","When an older house cannot be saved, we take it down and build new on the same lot, from foundation and steel to siding and finishes."),
         ("Primary baths","Gut remodels with waterproofed walk in showers, frameless glass and vanities built in our shop."),
         ("Kitchens in older homes","Opening up closed kitchens, adding islands and running new electric and plumbing behind plaster walls."),
         ("Rear additions","Family rooms, mudrooms and bigger kitchens added to the back of the house, with the roofline and siding tied in.")],
  permits='Garden City is an incorporated village, so building permits are filed with the Incorporated Village of Garden City building department rather than the Town of Hempstead. The village looks at exterior changes as well as structural work, so we confirm what applies to your project before the design is final, then handle filing and inspections through final sign off.',
  nearby=[("mineola","Mineola","just north, across Old Country Road"),("westbury","Westbury","a short drive east"),("rockville-centre","Rockville Centre","to the south")],
  faq=[("Are you working on any homes in Garden City right now?","Yes. HomeCore Construction has a custom home rebuild with a rear addition underway in Garden City, and we recently finished a master bathroom in the village. Both are shown on this page and in our Progress Stories."),
       ("Who handles permits for a remodel in Garden City?","Garden City is an incorporated village with its own building department. HomeCore Construction prepares the filing, works with the village through review and inspections, and takes the job to final sign off."),
       ("Can you match the trim and cabinetry in an older Garden City home?","Yes. Our cabinetry, vanities and trim are built in our own Long Island millwork shop, so we can match existing profiles and finishes in older colonials and Tudors."),
       ("Are you licensed in Nassau County?","Yes. HomeCore Construction holds Nassau County Home Improvement License 205185 and Suffolk County Home Improvement License HI-74242."),
       ("Do you give free estimates in Garden City?","Yes. HomeCore Construction gives free, in-home estimates. Call (516) 509-3289 or send us a message through the website.")],
  cta="Planning a Project in Garden City?",
 ),
 dict(
  slug="rockville-centre", name="Rockville Centre", short="Rockville Centre",
  title="Contractor in Rockville Centre, NY | Kitchens, Baths &amp; Additions | HomeCore Construction",
  desc="HomeCore Construction remodels kitchens and baths and builds additions and dormers for Rockville Centre village homes. Nassau County Home Improvement License 205185.",
  og=BASE + "/images/og-homecore.png",
  hero="Kitchens, baths, dormers and additions for the colonials, Tudors and Capes of Rockville Centre.",
  h2="Remodeling in Rockville Centre",
  intro=[
   'Rockville Centre is a walkable village built around its downtown and train station, with a mix of colonials, Tudors, Capes and Victorian era homes on modest lots. Many were built before World War II, and owners here tend to invest in the house they have rather than move: a new <a href="/kitchen-remodeling">kitchen</a>, a second <a href="/bathroom-remodeling">bathroom</a>, or more space upstairs.',
   'Because lots are tight, the usual way to grow a Rockville Centre home is up rather than out. A full or shed <a href="/home-additions">dormer</a> can turn a cramped Cape attic into real bedrooms and a bath, and a second story addition can transform a ranch. HomeCore Construction handles the structure, framing, roofing and finishes with one team.',
  ],
  types=[("Dormers and second stories","Shed dormers, full second floors and attic conversions that add bedrooms without giving up the yard."),
         ("Kitchens","Layout changes, islands where they fit and cabinetry built in our own shop to suit older room sizes."),
         ("Baths","Hall bath and primary bath remodels with new waterproofing, tile and vanities."),
         ("Porches and exteriors","Front porches, porticos, new siding, roofing and windows that suit a village street.")],
  permits='Rockville Centre is an incorporated village in the Town of Hempstead, and building permits go through the Village of Rockville Centre rather than the town. HomeCore Construction prepares the filing, coordinates the inspections and sees the job through to final sign off.',
  nearby=[("garden-city","Garden City","to the north, where we have a custom home underway"),("wantagh","Wantagh","east along the South Shore"),("mineola","Mineola","up the road in central Nassau")],
  faq=[("Do you build dormers in Rockville Centre?","Yes. Dormers and second story additions are one of the best ways to add space on a Rockville Centre lot. HomeCore Construction handles the structure, framing, roofing and interior finishes."),
       ("Who issues building permits in Rockville Centre?","Rockville Centre is an incorporated village, so permits are handled by the Village of Rockville Centre. HomeCore Construction prepares the filing and coordinates inspections through final sign off."),
       ("Are you licensed to work in Rockville Centre?","Yes. HomeCore Construction holds Nassau County Home Improvement License 205185."),
       ("Do you give free estimates?","Yes. HomeCore Construction gives free, in-home estimates. Call (516) 509-3289 or send us a message through the website.")],
  cta="Planning a Project in Rockville Centre?",
 ),
 dict(
  slug="mineola", name="Mineola", short="Mineola",
  title="Contractor in Mineola, NY | Dormers, Kitchens &amp; Baths | HomeCore Construction",
  desc="HomeCore Construction builds dormers and second stories and remodels kitchens and baths for Mineola Capes, colonials and high ranches. Free estimates.",
  og=BASE + "/images/og-homecore.png",
  hero="Dormers, second stories, kitchens and baths for the Capes, colonials and high ranches of Mineola.",
  h2="Remodeling in Mineola",
  intro=[
   'Mineola is the county seat of Nassau, a busy village around the train station with quieter residential blocks of Capes, colonials, high ranches and two family homes. Much of the housing dates from the early and middle 1900s, which means small kitchens, one full bath and attic space that is waiting to be used.',
   'That is where HomeCore Construction does its best work in a house like this: a <a href="/home-additions">dormer or second story</a> to add bedrooms, a reworked <a href="/kitchen-remodeling">kitchen</a> that opens to the dining room, or a second <a href="/bathroom-remodeling">bathroom</a>. We also take on <a href="/roofing-siding-windows">roofing, siding and windows</a> for homes that need an exterior refresh.',
  ],
  types=[("Dormers and second stories","More bedrooms and a second bath without adding to the footprint."),
         ("Kitchens","Opening closed kitchens to the dining room, new cabinetry from our shop and updated electric."),
         ("Baths","Full gut remodels and new second baths, tiled and waterproofed the right way."),
         ("Exteriors","Roofing, siding, windows and front entries.")],
  permits='Mineola is an incorporated village, so most projects are permitted through the Village of Mineola building department. Most of the village sits in the Town of North Hempstead, with a small part in the Town of Hempstead. HomeCore Construction confirms the right office for your address, prepares the filing and coordinates inspections through final sign off.',
  nearby=[("garden-city","Garden City","just south, where we have a custom home underway"),("westbury","Westbury","a few minutes east"),("manhasset","Manhasset","north toward the Sound")],
  faq=[("Can you add a dormer to my Mineola Cape?","Yes. A dormer or full second story is one of the most common ways to add bedrooms and a bath to a Mineola Cape. HomeCore Construction handles the structure, framing, roof and interior finishes."),
       ("Who handles building permits in Mineola?","Most Mineola homes are permitted through the Village of Mineola. HomeCore Construction prepares the filing and coordinates inspections through final sign off."),
       ("Are you licensed in Nassau County?","Yes. HomeCore Construction holds Nassau County Home Improvement License 205185."),
       ("Do you give free estimates?","Yes. HomeCore Construction gives free, in-home estimates. Call (516) 509-3289 or send us a message through the website.")],
  cta="Planning a Project in Mineola?",
 ),
 dict(
  slug="westbury", name="Westbury", short="Westbury",
  title="Contractor in Westbury, NY | Additions, Kitchens &amp; Exteriors | HomeCore Construction",
  desc="HomeCore Construction builds additions and remodels kitchens, baths and exteriors for homes in Westbury and the surrounding area. Free estimates.",
  og=BASE + "/images/og-homecore.png",
  hero="Additions, kitchens, baths and exterior work for Westbury homes and the neighborhoods around them.",
  h2="Remodeling in Westbury",
  intro=[
   'Westbury mixes postwar Capes and ranches with older colonials near the village center and the train station. Many homes still have their original layout: a closed kitchen, one bath and bedrooms that are smaller than families need today. HomeCore Construction helps owners make those houses work, with <a href="/home-additions">additions</a>, reworked <a href="/kitchen-remodeling">kitchens</a> and new <a href="/bathroom-remodeling">baths</a>.',
   'Exterior work is a big part of the picture too. Older Westbury homes often need a new roof, siding and windows at the same time, and doing them together with one crew keeps the flashing, trim and details tight. See our <a href="/roofing-siding-windows">roofing, siding and windows</a> page for how we approach it.',
  ],
  types=[("Additions","Rear additions and second floors that give a Cape or ranch the space of a larger home."),
         ("Kitchens and baths","New layouts, cabinetry from our shop, tile and fixtures."),
         ("Roofing, siding and windows","Complete exterior updates done by one team, so the details line up."),
         ("Garage conversions","Turning an attached garage into a family room, office or bedroom.")],
  permits='The Village of Westbury sits mostly in the Town of North Hempstead, with a small part in the Town of Oyster Bay, and has its own building department. Some homes with a Westbury mailing address are outside the village, where the town handles permits instead. HomeCore Construction confirms which office covers your address, prepares the filing and coordinates inspections through final sign off.',
  nearby=[("mineola","Mineola","a few minutes west"),("garden-city","Garden City","to the southwest, where we have a custom home underway"),("oyster-bay","Oyster Bay","north toward the Sound")],
  faq=[("Who issues permits for a Westbury remodel?","Homes inside the Village of Westbury are permitted through the village building department. Homes outside the village line generally go through the town. HomeCore Construction confirms which applies and handles the filing."),
       ("Do you build additions in Westbury?","Yes. HomeCore Construction builds rear additions and second floors, from foundation and framing to roofing, siding and interior finishes."),
       ("Are you licensed in Nassau County?","Yes. HomeCore Construction holds Nassau County Home Improvement License 205185."),
       ("Do you give free estimates?","Yes. HomeCore Construction gives free, in-home estimates. Call (516) 509-3289 or send us a message through the website.")],
  cta="Planning a Project in Westbury?",
 ),
 dict(
  slug="manhasset", name="Manhasset", short="Manhasset",
  title="Contractor in Manhasset, NY | Kitchens, Millwork &amp; Custom Homes | HomeCore Construction",
  desc="HomeCore Construction builds kitchens, primary baths, custom millwork, additions and custom homes for Manhasset colonials and Tudors. Free estimates.",
  og=BASE + "/images/og-homecore.png",
  hero="Kitchens, primary baths, custom millwork and custom homes for Manhasset colonials and Tudors.",
  h2="Building and Remodeling in Manhasset",
  intro=[
   'Manhasset on the North Shore is known for its center hall colonials, Tudors and stone and brick homes, many on generous lots with mature trees. Owners here usually want work that matches the quality of the house: a <a href="/kitchen-remodeling">kitchen</a> with real furniture grade cabinetry, a <a href="/bathroom-remodeling">primary bath</a> done with care, or a <a href="/custom-homes">new custom home</a> where an older house has reached the end of its life.',
   'Our <a href="/custom-millwork">custom millwork</a> is built in our own Long Island shop: inset cabinetry, paneled walls, coffered ceilings, built ins and butler&#39;s pantries. In a Manhasset home that kind of work is often what ties a renovation back to the original house.',
  ],
  types=[("Kitchens","Inset and painted cabinetry from our shop, large islands and pantries."),
         ("Custom millwork","Libraries, paneled rooms, coffered ceilings, mudrooms and built ins."),
         ("Primary baths","Gut remodels with tiled showers, frameless glass and custom vanities."),
         ("Custom homes and additions","Ground up homes and large additions that respect the character of the street.")],
  permits='Manhasset is an unincorporated hamlet in the Town of North Hempstead, so most homes are permitted through the Town of North Hempstead building department. Nearby villages such as Plandome, Munsey Park and Flower Hill have their own building departments. HomeCore Construction confirms which office covers your address, prepares the filing and coordinates inspections through final sign off.',
  nearby=[("port-washington","Port Washington","next door on the peninsula to the north"),("great-neck","Great Neck","just west across Manhasset Bay"),("mineola","Mineola","to the south in central Nassau")],
  faq=[("Who issues building permits in Manhasset?","Most of Manhasset is unincorporated and permitted through the Town of North Hempstead. Homes in nearby incorporated villages, such as Plandome, Munsey Park and Flower Hill, go through those villages instead. HomeCore Construction confirms which applies and handles the filing."),
       ("Can you build custom cabinetry and millwork for a Manhasset home?","Yes. HomeCore Construction builds cabinetry, paneling, coffered ceilings and built ins in our own Long Island shop and installs them with the same team."),
       ("Are you licensed in Nassau County?","Yes. HomeCore Construction holds Nassau County Home Improvement License 205185."),
       ("Do you give free estimates?","Yes. HomeCore Construction gives free, in-home estimates. Call (516) 509-3289 or send us a message through the website.")],
  cta="Planning a Project in Manhasset?",
 ),
 dict(
  slug="massapequa", name="Massapequa", short="Massapequa",
  title="Contractor in Massapequa, NY | Second Stories, Kitchens &amp; Exteriors | HomeCore Construction",
  desc="HomeCore Construction builds second story additions and dormers and remodels kitchens, baths and exteriors for Massapequa homes. Free estimates.",
  og=BASE + "/images/og-homecore.png",
  hero="Second stories, dormers, kitchens, baths and exteriors for the Capes, ranches and high ranches of Massapequa.",
  h2="Remodeling in Massapequa",
  intro=[
   'Massapequa grew fast after World War II, and its streets are lined with the Capes, ranches, high ranches and split levels of that era. Those homes have good bones but small rooms, so the most common project here is going up: a <a href="/home-additions">second story addition</a> or a full dormer that doubles the living space without losing the yard.',
   'South of Merrick Road many homes sit close to the canals and bay, and owners there often combine a renovation with new <a href="/roofing-siding-windows">roofing, siding and windows</a> or a rebuilt <a href="/decks-porches">deck</a> for the backyard. HomeCore Construction handles structure, exterior and interior with one team.',
  ],
  types=[("Second story additions","Turning a ranch or Cape into a full two story home."),
         ("Dormers","Shed and full dormers that add bedrooms and a bath upstairs."),
         ("Exteriors and decks","Roofing, siding, windows and composite decks built by our own carpenters."),
         ("Kitchens and baths","Full remodels with cabinetry and vanities from our shop.")],
  permits='Most of Massapequa is unincorporated and part of the Town of Oyster Bay, so permits generally go through the Town of Oyster Bay building department. Massapequa Park is a separate incorporated village with its own building department. HomeCore Construction confirms which applies to your address, prepares the filing and coordinates inspections through final sign off.',
  nearby=[("wantagh","Wantagh","just west along the South Shore"),("oyster-bay","Oyster Bay","the same town, up on the North Shore"),("westbury","Westbury","north in central Nassau")],
  faq=[("Do you build second story additions in Massapequa?","Yes. Second story additions and dormers are some of the most common projects on Massapequa ranches and Capes. HomeCore Construction handles the structure, framing, roofing and interior finishes."),
       ("Who handles permits for Massapequa homes?","Most Massapequa homes are permitted through the Town of Oyster Bay. Homes in the Village of Massapequa Park go through the village. HomeCore Construction confirms which applies and handles the filing."),
       ("Are you licensed in Nassau County?","Yes. HomeCore Construction holds Nassau County Home Improvement License 205185."),
       ("Do you give free estimates?","Yes. HomeCore Construction gives free, in-home estimates. Call (516) 509-3289 or send us a message through the website.")],
  cta="Planning a Project in Massapequa?",
 ),
 dict(
  slug="wantagh", name="Wantagh", short="Wantagh",
  title="Contractor in Wantagh, NY | Additions, Kitchens &amp; Baths | HomeCore Construction",
  desc="HomeCore Construction builds additions and dormers and remodels kitchens, baths, decks and exteriors for Wantagh homes. Free estimates.",
  og=BASE + "/images/og-homecore.png",
  hero="Additions, dormers, kitchens, baths and decks for Wantagh homes, north and south of Sunrise Highway.",
  h2="Remodeling in Wantagh",
  intro=[
   'Wantagh is a South Shore community of Capes, ranches, high ranches and colonials, most built in the decades after the war, with waterfront streets south of Merrick Road. Families tend to stay a long time, so the house has to keep up: a bigger <a href="/kitchen-remodeling">kitchen</a>, an updated <a href="/bathroom-remodeling">bath</a> or a whole new floor.',
   'HomeCore Construction builds <a href="/home-additions">second stories, dormers and rear additions</a>, and we finish the inside with cabinetry and vanities from our own shop. Outside, we build <a href="/decks-porches">decks and front porches</a> and replace <a href="/roofing-siding-windows">roofing, siding and windows</a>.',
  ],
  types=[("Second stories and dormers","More bedrooms and baths on a ranch, Cape or high ranch."),
         ("Kitchens","Opening walls, adding islands and new cabinetry from our shop."),
         ("Decks and porches","Composite decks, covered porches and front entries."),
         ("Whole home renovations","Gut renovations that update everything from framing to finishes.")],
  permits='Wantagh is an unincorporated hamlet in the Town of Hempstead, so building permits generally go through the Town of Hempstead building department. HomeCore Construction prepares the filing, coordinates inspections and takes the job through final sign off.',
  nearby=[("massapequa","Massapequa","just east along the South Shore"),("rockville-centre","Rockville Centre","to the west"),("garden-city","Garden City","north in central Nassau, where we have a custom home underway")],
  faq=[("Who handles building permits in Wantagh?","Wantagh is part of the Town of Hempstead, so permits generally go through the Town of Hempstead building department. HomeCore Construction prepares the filing and coordinates inspections."),
       ("Can you add a second floor to a Wantagh ranch?","Yes. HomeCore Construction builds second story additions and dormers, from structural work and framing to roofing and interior finishes."),
       ("Are you licensed in Nassau County?","Yes. HomeCore Construction holds Nassau County Home Improvement License 205185."),
       ("Do you give free estimates?","Yes. HomeCore Construction gives free, in-home estimates. Call (516) 509-3289 or send us a message through the website.")],
  cta="Planning a Project in Wantagh?",
 ),
 dict(
  slug="oyster-bay", name="Oyster Bay", short="Oyster Bay",
  title="Contractor in Oyster Bay, NY | Renovations, Millwork &amp; Custom Homes | HomeCore Construction",
  desc="HomeCore Construction renovates older homes and builds custom millwork, additions and custom homes in Oyster Bay and the North Shore. Free estimates.",
  og=BASE + "/images/og-homecore.png",
  hero="Renovations, additions, custom millwork and custom homes for Oyster Bay and the North Shore.",
  h2="Building and Remodeling in Oyster Bay",
  intro=[
   'Oyster Bay is one of the oldest communities on Long Island, a harbor hamlet with colonial era and Victorian homes near the water and larger estate properties in the hills around it. Older houses here call for a builder who can open walls carefully, rebuild what is behind them and match the trim and detail that make the house what it is.',
   'HomeCore Construction takes on <a href="/whole-home-renovation">whole home renovations</a>, <a href="/home-additions">additions</a> and <a href="/custom-homes">custom homes</a>, and our <a href="/custom-millwork">custom millwork</a> is built in our own Long Island shop, so new cabinetry, paneling and trim can be made to fit an older house.',
  ],
  types=[("Whole home renovations","Gut renovations of older homes, from framing and mechanicals to finishes."),
         ("Custom millwork","Cabinetry, paneling, built ins and trim made to match the house."),
         ("Additions","Additions that tie into the existing roofline and siding."),
         ("Custom homes","Ground up homes on North Shore lots.")],
  permits='The hamlet of Oyster Bay is part of the Town of Oyster Bay, which generally handles building permits for unincorporated areas. Nearby incorporated villages, such as Oyster Bay Cove, Cove Neck and Bayville, have their own building departments. HomeCore Construction confirms which office covers your address, prepares the filing and coordinates inspections through final sign off.',
  nearby=[("cold-spring-harbor","Cold Spring Harbor","just east across the county line, where we built custom millwork"),("westbury","Westbury","south in central Nassau"),("massapequa","Massapequa","the same town, down on the South Shore")],
  faq=[("Do you renovate older homes in Oyster Bay?","Yes. HomeCore Construction takes on whole home renovations and additions on older homes, and builds matching trim, cabinetry and paneling in our own millwork shop."),
       ("Who handles building permits in Oyster Bay?","Unincorporated areas, including the hamlet of Oyster Bay, generally go through the Town of Oyster Bay. Incorporated villages nearby have their own building departments. HomeCore Construction confirms which applies and handles the filing."),
       ("Are you licensed in Nassau County?","Yes. HomeCore Construction holds Nassau County Home Improvement License 205185 and Suffolk County Home Improvement License HI-74242, so we work on both sides of the county line."),
       ("Do you give free estimates?","Yes. HomeCore Construction gives free, in-home estimates. Call (516) 509-3289 or send us a message through the website.")],
  cta="Planning a Project in Oyster Bay?",
 ),
 dict(
  slug="port-washington", name="Port Washington", short="Port Washington",
  title="Contractor in Port Washington, NY | Kitchens, Baths &amp; Additions | HomeCore Construction",
  desc="HomeCore Construction remodels kitchens and baths and builds additions and custom homes on the Port Washington peninsula. Free estimates.",
  og=BASE + "/images/og-homecore.png",
  hero="Kitchens, baths, additions and custom homes across the Port Washington peninsula.",
  h2="Remodeling in Port Washington",
  intro=[
   'Port Washington covers a whole peninsula on Manhasset Bay, with older colonials and Tudors near the town dock and the train station, midcentury homes in the neighborhoods above, and waterfront houses along the shore. That variety means every project starts with understanding the house: its age, its structure and what the owners want from it.',
   'HomeCore Construction remodels <a href="/kitchen-remodeling">kitchens</a> and <a href="/bathroom-remodeling">baths</a>, builds <a href="/home-additions">additions</a> and <a href="/custom-homes">custom homes</a>, and makes cabinetry and built ins in our own <a href="/custom-millwork">millwork shop</a>. Exterior work like <a href="/roofing-siding-windows">roofing, siding and windows</a> is done by the same team.',
  ],
  types=[("Kitchens","Open layouts, islands and cabinetry built in our shop."),
         ("Baths","Primary and hall baths with waterproofed showers, tile and custom vanities."),
         ("Additions","Second floors and rear additions on midcentury and older homes."),
         ("Custom homes","New homes built from the foundation up.")],
  permits='Much of Port Washington is unincorporated and permitted through the Town of North Hempstead. The peninsula also includes incorporated villages, such as Sands Point, Manorhaven and Baxter Estates, each with its own building department. HomeCore Construction confirms which office covers your address, prepares the filing and coordinates inspections through final sign off.',
  nearby=[("manhasset","Manhasset","just south"),("great-neck","Great Neck","across Manhasset Bay to the west"),("oyster-bay","Oyster Bay","east along the North Shore")],
  faq=[("Who issues building permits in Port Washington?","It depends on the address. Unincorporated areas go through the Town of North Hempstead, while the incorporated villages on the peninsula have their own building departments. HomeCore Construction confirms which applies and handles the filing."),
       ("Do you build additions in Port Washington?","Yes. HomeCore Construction builds second floors and rear additions, from foundation and framing to roofing, siding and interior finishes."),
       ("Are you licensed in Nassau County?","Yes. HomeCore Construction holds Nassau County Home Improvement License 205185."),
       ("Do you give free estimates?","Yes. HomeCore Construction gives free, in-home estimates. Call (516) 509-3289 or send us a message through the website.")],
  cta="Planning a Project in Port Washington?",
 ),
 dict(
  slug="great-neck", name="Great Neck", short="Great Neck",
  title="Contractor in Great Neck, NY | Custom Homes, Kitchens &amp; Baths | HomeCore Construction",
  desc="HomeCore Construction builds custom homes and additions and remodels kitchens and baths across the Great Neck peninsula and its villages. Free estimates.",
  og=BASE + "/images/og-homecore.png",
  hero="Custom homes, additions, kitchens and baths across the Great Neck peninsula and its villages.",
  h2="Building and Remodeling in Great Neck",
  intro=[
   'The Great Neck peninsula is a collection of villages and neighborhoods, from the colonials and Tudors near the train station to larger homes on bigger lots toward Kings Point. Many owners here are rebuilding or substantially expanding older houses, and the work calls for a contractor who can carry a project from foundation to finished millwork.',
   'HomeCore Construction builds <a href="/custom-homes">custom homes</a> and <a href="/home-additions">additions</a>, remodels <a href="/kitchen-remodeling">kitchens</a> and <a href="/bathroom-remodeling">baths</a>, and makes cabinetry, paneling and built ins in our own <a href="/custom-millwork">Long Island shop</a>.',
  ],
  types=[("Custom homes","New homes where an older house has reached the end of its life."),
         ("Additions","Second floors and large rear additions."),
         ("Kitchens and millwork","Kitchens and built ins from our own shop."),
         ("Primary baths","Gut remodels with tiled showers, frameless glass and custom vanities.")],
  permits='The Great Neck area includes nine incorporated villages, such as Great Neck, Great Neck Plaza, Great Neck Estates, Kings Point and Russell Gardens, each with its own building department, plus unincorporated areas that go through the Town of North Hempstead. HomeCore Construction confirms which office covers your address, prepares the filing and coordinates inspections through final sign off.',
  nearby=[("manhasset","Manhasset","just east"),("port-washington","Port Washington","across Manhasset Bay"),("mineola","Mineola","south in central Nassau")],
  faq=[("Which building department covers my Great Neck home?","It depends on the village. Great Neck has nine incorporated villages with their own building departments, and unincorporated areas are covered by the Town of North Hempstead. HomeCore Construction confirms which applies and handles the filing."),
       ("Do you build custom homes in Great Neck?","Yes. HomeCore Construction builds ground up custom homes and large additions, with cabinetry and millwork from our own shop."),
       ("Are you licensed in Nassau County?","Yes. HomeCore Construction holds Nassau County Home Improvement License 205185."),
       ("Do you give free estimates?","Yes. HomeCore Construction gives free, in-home estimates. Call (516) 509-3289 or send us a message through the website.")],
  cta="Planning a Project in Great Neck?",
 ),
]

def jsonld(t):
    url = f"{BASE}/areas-we-serve/{t['slug']}"
    m = re.search(r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>', TEMPLATE, re.S)
    data = json.loads(m.group(1))
    biz = data["@graph"][0]
    # Keep every Nassau town page in the company areaServed list, matching the rest of the site.
    names = {a.get("name") for a in biz.get("areaServed", [])}
    for town in TOWNS:
        if f"{town['name']}, NY" not in names:
            biz["areaServed"].append({"@type": "Place", "name": f"{town['name']}, NY"})
    title_plain = html.unescape(t["title"])
    graph = [biz,
     {"@type": "WebPage", "@id": url, "url": url, "name": title_plain, "description": t["desc"],
      "about": {"@id": f"{BASE}/#business"}, "spatialCoverage": {"@type": "Place", "name": f"{t['name']}, NY"}},
     {"@type": "BreadcrumbList", "itemListElement": [
       {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE}/"},
       {"@type": "ListItem", "position": 2, "name": "Areas We Serve", "item": f"{BASE}/areas-we-serve/"},
       {"@type": "ListItem", "position": 3, "name": t["name"], "item": url}]},
     {"@type": "FAQPage", "mainEntity": [
       {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in t["faq"]]}]
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, indent=1, ensure_ascii=False)

def head(t):
    h = TEMPLATE.split("<header class=\"page-hero\">")[0]
    url = f"{BASE}/areas-we-serve/{t['slug']}"
    h = re.sub(r"<title>.*?</title>", f"<title>{t['title']}</title>", h, flags=re.S)
    desc = html.escape(t["desc"], quote=True)
    h = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + desc, h)
    h = re.sub(r'(<meta (?:property|name)="(?:og|twitter):description" content=")[^"]*', lambda m: m.group(1) + desc, h)
    h = re.sub(r'(<meta (?:property|name)="(?:og|twitter):title" content=")[^"]*', lambda m: m.group(1) + t["title"], h)
    h = re.sub(r'(<meta property="og:image:alt" content=")[^"]*', lambda m: m.group(1) + t["title"], h)
    h = re.sub(r'(<meta (?:property|name)="(?:og|twitter):image" content=")[^"]*', lambda m: m.group(1) + t["og"], h)
    h = re.sub(r'(<link rel="canonical" href=")[^"]*', lambda m: m.group(1) + url, h)
    h = re.sub(r'(<meta property="og:url" content=")[^"]*', lambda m: m.group(1) + url, h)
    h = re.sub(r'<script type="application/ld\+json">.*?</script>',
               lambda m: '<script type="application/ld+json">\n' + jsonld(t) + '\n  </script>', h, count=1, flags=re.S)
    h = h.replace("  </style>\n  <link rel=\"stylesheet\"", TOWN_GRID_CSS + "  </style>\n  <link rel=\"stylesheet\"", 1)
    return h

def body(t):
    n = t["name"]
    out = [f'''<header class="page-hero">
  <p class="crumbs"><a href="/">Home</a> &rsaquo; <a href="/areas-we-serve/">Areas We Serve</a> &rsaquo; {n}</p>
  <span class="hero-eyebrow">Nassau County</span>
  <h1>{n}</h1>
  <p>{t["hero"]}</p>
  <div class="hero-actions">
    <a href="tel:5165093289" class="btn-solid">Call (516) 509-3289</a>
    <a href="/#quote" class="btn-outline-white">Get a Free Estimate</a>
  </div>
</header>
<section>
  <div class="wrap prose" style="max-width:820px">
    <div class="center"><p class="section-eyebrow">{n}</p><h2>{t["h2"]}</h2></div>
''' + "\n".join(f"    <p>{p}</p>" for p in t["intro"]) + "\n  </div>\n</section>"]
    for j in t.get("jobs", []):
        links = " ".join(f'<a href="{u}" class="btn-outline-navy">{l}</a>' for u, l in j["links"])
        out.append(f'''<section class="alt-bg">
  <div class="wrap">
    <div class="center"><p class="section-eyebrow">{j["eyebrow"]}</p><h2>{j["h2"]}</h2></div>
    <p class="section-sub">{j["sub"]}</p>
    <div class="stages">
      ''' + "\n      ".join(j["imgs"]) + f'''
    </div>
    <p class="center" style="margin-top:34px">{links}</p>
  </div>
</section>''')
    cards = "".join(f"<div><h3>{a}</h3><p>{b}</p></div>" for a, b in t["types"])
    out.append(f'''<section{' class="alt-bg"' if not t.get("jobs") else ''}>
  <div class="wrap">
    <div class="center"><p class="section-eyebrow">Common Projects</p><h2>What We Build in {n}</h2></div>
    <div class="town-grid">{cards}</div>
  </div>
</section>
<section>
  <div class="wrap prose" style="max-width:820px">
    <div class="center"><p class="section-eyebrow">Permits</p><h2>Permits and Approvals in {n}</h2></div>
    <p>{t["permits"]}</p>
    <p>HomeCore Construction holds {LICENSE} and Suffolk County Home Improvement License HI-74242.</p>
  </div>
</section>''')
    near = "".join(f'<div><h3>{NAMES[s]}</h3><p>{NAMES[s]} is {d}.</p><a class="more" href="/areas-we-serve/{s}">{NAMES[s]} page &rarr;</a></div>' for s, _, d in t["nearby"])
    out.append(f'''<section class="alt-bg">
  <div class="wrap">
    <div class="center"><p class="section-eyebrow">Nearby</p><h2>Nearby Towns We Serve</h2></div>
    <div class="town-grid">{near}</div>
    <p class="center" style="margin-top:34px"><a href="/areas-we-serve/" class="btn-outline-navy">All Areas We Serve</a></p>
  </div>
</section>''')
    faq = "\n".join(f"    <details><summary>{html.escape(q, quote=False)}</summary><p>{html.escape(a, quote=False)}</p></details>" for q, a in t["faq"])
    out.append(f'''<section>
  <div class="wrap">
    <div class="center"><p class="section-eyebrow">Questions</p><h2>Questions From {n} Homeowners</h2></div>
    <div class="faq">
{faq}
    </div>
  </div>
</section>
<section class="alt-bg">
  <div class="wrap center">
    <p class="section-eyebrow">Keep Exploring</p><h2>Services for {n} Homes</h2>
    <p class="section-sub">Every service, one team.</p>
    <div class="related">
      <a href="/kitchen-remodeling" class="btn-outline-navy">Kitchens</a>
      <a href="/bathroom-remodeling" class="btn-outline-navy">Baths</a>
      <a href="/home-additions" class="btn-outline-navy">Additions</a>
      <a href="/custom-homes" class="btn-outline-navy">Custom Homes</a>
      <a href="/whole-home-renovation" class="btn-outline-navy">Whole Home</a>
      <a href="/custom-millwork" class="btn-outline-navy">Millwork</a>
      <a href="/decks-porches" class="btn-outline-navy">Decks &amp; Porches</a>
      <a href="/roofing-siding-windows" class="btn-outline-navy">Roofing &amp; Siding</a>
      <a href="/garage-conversions" class="btn-outline-navy">Garage Conversions</a>
    </div>
  </div>
</section>
<section class="services-cta">
  <h2>{t["cta"]}</h2>
  <p>Call or send us a message and we will set up a time to come out. Estimates are always free and always honest.</p>
  <div class="services-cta-actions">
    <a href="tel:5165093289" class="btn-solid">Call (516) 509-3289</a>
    <a href="/#quote" class="btn-outline-navy">Get a Free Estimate</a>
  </div>
</section>
''')
    return "\n".join(out)

def foot():
    return "\n<footer>" + TEMPLATE.split("<footer>", 1)[1]

if __name__ == "__main__":
    for t in TOWNS:
        page = head(t) + body(t) + foot()
        (ROOT / "areas-we-serve" / f"{t['slug']}.html").write_text(page)
        print("wrote", t["slug"])
