#!/usr/bin/env python3
"""Cooper Crane page engine.

Builds, from one source of truth:
  assets/site.css                       shared stylesheet (homepage styles + subpage styles)
  /services/{service}/                  6 service pages   (depth layer)
  /service-areas/                       areas hub
  /service-areas/{area}/                8 area pages      (breadth layer)
  /services/{service}-in-{area}/        48 combos         (anchor matrix)

Every subpage sits at depth 2, so the link prefix is always ../../
"""
import os, json, shutil

PRE = '../../'
ASSET_V = '9'   # bump on every site.css / site.js change (busts the CDN + phone cache)
BASE = 'https://coopercrane.com/'
PHONE_D = '(954) 445-6186'
PHONE_H = '+19544456186'
EMAIL = 'Coopercranefl@gmail.com'

# ---------------------------------------------------------------- services
SERVICES = [
 dict(slug='ac-unit-lifts', nav='AC Units', short='AC unit lifts',
  name='Rooftop AC Unit Lifts', pre='Rooftop AC unit', img='cc-rooftop-lift.jpg',
  alt='Cooper Crane boom truck setting a rooftop AC unit in Southeast Florida',
  cap='Boom truck making a rooftop set on the Atlantic coast.',
  blurb='Rooftop condensers and air handlers set clean on the curb, single homes to high-rises.',
  lede='HVAC crews call us more than anyone else. Condensers, air handlers and full package units set straight onto the curb, on single-family roofs and on high-rise decks.',
  intro='<p>An AC change-out lives or dies on the lift. The unit has to come off the truck, clear the roofline, and land square on a curb that is often the same footprint as the crate. <strong>We do this several times a week</strong>, so the part your crew is worried about is the part we do every day.</p><p>Most residential change-outs are a 17-ton boom truck and under two hours on site. Commercial package units, tight courtyards, and anything past the second floor is where the 35-ton and 40-ton machines earn their keep.</p>',
  h2a='What we need before we roll',
  pts=[('Unit weight','Off the spec sheet or the crate label. Most residential condensers run 150 to 400 lb; commercial packages go well past a ton.'),
       ('Roof height and setback','How high the deck is and how far in from the curb line the unit has to travel.'),
       ('Where the truck can sit','Driveway, street, alley. Overhead power lines are the single biggest thing that changes the plan.'),
       ('Curb ready or not','If the curb or pad is not finished we can still set it aside, but you will pay for a second trip.')],
  h2b='How it usually runs',
  outro='<p>We show up, set outriggers, and your crew rigs while we spec the pick. Old unit comes off, new unit goes on, we pull the boom in and clear the site. Most single change-outs are done inside a two-hour window, which is why we can usually fit an emergency into the same week.</p><p>If a tenant is without cooling, say so when you call. We will tell you honestly whether we can get there today or whether you are better off calling someone else.</p>',
  spec=[('Typical machine','17-ton boom truck'),('Common weight range','150 lb to 2+ tons'),('Usual time on site','1 to 2 hours'),('Operator','Certified, included')],
  kw='ac unit crane lift, rooftop hvac crane, condenser lift, air handler crane'),

 dict(slug='pest-control-tarp-lifts', nav='Tarp Lifts', short='fumigation tarp lifts',
  name='Pest-Control Tarp Lifts', pre='Pest-control tarps', img='work-residential.jpg',
  alt='Cooper Crane boom truck working over a Southeast Florida residential roofline',
  cap='Working over a residential roofline in Broward County.',
  blurb='Fumigation tenting lifted up and over the roofline so tarp crews work fast and safe.',
  lede='Tenting a two-story house by hand is slow, and it is where crews get hurt. We fly the tarps over the ridge so your team stays on the ground and the tent goes up in a fraction of the time.',
  intro='<p>Fumigation companies were some of Cooper Crane\'s first steady customers, and it is still one of the lifts we are called for most. <strong>The crane does the dangerous part</strong>: getting heavy, wind-catching tarps up and over a roofline without dragging them across tile or shingle.</p><p>We work to your schedule, not ours. Most tent jobs are early-morning starts so the structure is sealed before the day heats up, and we plan the pick around your seal-and-clamp crew.</p>',
  h2a='What makes a tarp job go smoothly',
  pts=[('Roof pitch and height','Steep tile roofs need a higher pick point so nothing drags. Tell us the storey count and roof type.'),
       ('Wind','The reason tarp lifts get rescheduled. We will call it honestly rather than fight a gusty morning.'),
       ('Truck access','Driveways are usually fine. Tight cul-de-sacs and narrow easements may push us to the spider crane.'),
       ('Your crew size','We lift, you seal. The faster your ground crew clamps, the shorter the bill.')],
  h2b='Repeat work, standing arrangements',
  outro='<p>If you tent regularly we would rather set up a standing arrangement than quote you one house at a time. Several South Florida pest-control companies have run with us for years on that basis, and it means your jobs get slotted first when the schedule tightens.</p><p>Call the yard with your typical volume and we will talk through what that looks like.</p>',
  spec=[('Typical machine','17-ton boom truck'),('Best for','1 to 3 storey structures'),('Scheduling','Early-morning starts'),('Repeat volume','Standing arrangements available')],
  kw='fumigation tarp crane, tenting crane, pest control crane lift'),

 dict(slug='truss-setting', nav='Trusses', short='truss setting',
  name='Roof &amp; Floor Truss Setting', pre='Trusses or roofing material', img='work-boom-yard.jpg',
  alt='Cooper Crane Peterbilt boom truck staged with the boom extended for a truss set',
  cap='Boom truck staged and ready for a truss package.',
  blurb='Roof and floor trusses flown to your framing crew on schedule, not stacked in the yard.',
  lede='Your framing crew is only as fast as the truss on the hook. We keep the packages moving so the crew stays on the wall plate instead of standing around waiting.',
  intro='<p>Truss setting is a rhythm job. The crane is not the expensive part of the day; <strong>an idle framing crew is</strong>. That is why we would rather talk through the sequence before we arrive than figure it out on site with six guys on the clock.</p><p>Send the truss layout ahead if you have it. Knowing the longest span and the heaviest single truss lets us bring one machine that can reach the far gable instead of two that cannot.</p>',
  h2a='Plan the set before the truck rolls',
  pts=[('Longest span and heaviest truss','These two numbers pick the machine. Everything else is detail.'),
       ('Where the bundles are stacked','If the delivery dropped them on the far side of the lot, that is extra picks and extra hours.'),
       ('Crane position','We need a spot that reaches both gable ends without repositioning if we can get one.'),
       ('Crew readiness','Wall plates ready, bracing on hand. We can set fast, but only as fast as the crew ties off.')],
  h2b='Girder trusses and the awkward ones',
  outro='<p>Multi-ply girder trusses, long-span commercial packages and anything that has to fly over an existing structure are where we bring the 35-ton or the 40-ton out. Those are also the picks where an experienced operator matters most, and every Cooper Crane machine comes with one.</p><p>If you are bidding a job and need a crane number to price it, call before you submit. We will give you a real figure, not a placeholder.</p>',
  spec=[('Typical machine','17 to 40 ton, span dependent'),('Best sent ahead','Truss layout / span sheet'),('Usual time on site','Half day to full day'),('Operator','Certified, included')],
  kw='truss setting crane, roof truss crane, framing crane, floor truss lift'),

 dict(slug='roofing-material-lifts', nav='Roofing', short='roofing material lifts',
  name='Roofing Material Lifts', pre='Trusses or roofing material', img='cc-boom-truck.jpg',
  alt='A branded Cooper Crane Peterbilt boom truck working a Southeast Florida job site',
  cap='Cooper Crane iron on a Southeast Florida job site.',
  blurb='Tile and shingle bundles hoisted straight to the deck, not carried up a ladder.',
  lede='Carrying tile up a ladder is the slowest and most expensive way to load a roof. We put the whole pallet on the deck in one pick, where your crew wants it.',
  intro='<p>South Florida runs on tile, and tile is heavy. A single pallet of concrete tile can run north of 3,000 lb, which is a full morning of ladder work for a crew that should be laying underlayment instead.</p><p><strong>One crane, one morning, and the roof is loaded.</strong> We spot pallets where the crew is working rather than dumping everything at one corner, which keeps the load spread across the structure and keeps your guys from dragging tile across a finished field.</p>',
  h2a='Getting the load placement right',
  pts=[('Tile or shingle, and how much','Pallet count and material type. Concrete, clay and metal all load differently.'),
       ('Where each stack goes','Spreading the load matters structurally and saves your crew hours of walking.'),
       ('Roof condition','If we are loading over a finished or fragile field, tell us before we swing.'),
       ('Delivery timing','Best case, the material truck and the crane are on site in the same window.')],
  h2b='Tear-off and debris',
  outro='<p>The lift works in both directions. If you are tearing off, we can bring the old material down in bins instead of down a chute, which is faster on a tight lot and a lot cleaner on a finished driveway.</p><p>Tell us on the call whether you want the crane for load-up, tear-off, or both, and we will price the whole window rather than nickel and diming each pick.</p>',
  spec=[('Typical machine','17-ton boom truck'),('Common pallet weight','2,000 to 3,500 lb'),('Usual time on site','2 to 4 hours'),('Also handles','Tear-off debris bins')],
  kw='roofing crane lift, tile loading crane, shingle lift, roof loading crane'),

 dict(slug='generator-lifts', nav='Generators', short='generator lifts',
  name='Generator Lifts', pre='Generator', img='work-generator.jpg',
  alt='Cooper Crane boom truck setting a large industrial generator in Southeast Florida',
  cap='Setting an industrial generator in Southeast Florida.',
  blurb='Standby sets onto pads and rooftops without the wrestling match.',
  lede='Generators are dense, awkward and expensive. They also tend to live in the worst possible spot: a side yard behind a fence, or a roof deck four storeys up.',
  intro='<p>Hurricane season keeps this one busy. Residential standby units, commercial sets and rooftop installs all come down to the same problem: <strong>a very heavy object that has to land exactly on the anchor bolts</strong>, often over a wall, a pool cage or a finished driveway.</p><p>We set them slow and we set them square. An operator who rushes a generator pick is how pads get cracked and how enclosures get scratched before the thing has ever run.</p>',
  h2a='What we ask about first',
  pts=[('Dry weight of the set','Off the nameplate or the spec sheet. Residential standby is often 400 to 800 lb; commercial sets run several tons.'),
       ('Pad or roof, and how far in','Reach is usually the constraint, not capacity. A light unit far from the truck needs a bigger machine than a heavy one up close.'),
       ('What we have to clear','Pool cages, walls, fences, awnings and power lines all change the pick.'),
       ('Anchor set ready','If the pad is poured and the bolts are set, we can land it once and be done.')],
  h2b='Rooftop and platform sets',
  outro='<p>Rooftop generator work is the 35-ton and 40-ton end of our fleet, and it is the kind of lift where the crane has to reach high and far at the same time. Send a photo of the building and the intended location and we will tell you straight whether it is a one-crane job.</p><p>For emergency replacement after a storm, call the yard directly. Schedules move fast in that window and the phone gets you a real answer quicker than a form.</p>',
  spec=[('Typical machine','17 to 40 ton, reach dependent'),('Residential standby','Often 400 to 800 lb'),('Send if you can','Photo of the site and pad'),('Storm season','Call, do not email')],
  kw='generator crane lift, standby generator placement, industrial generator crane'),

 dict(slug='spider-crane-tight-access', nav='Spider Crane', short='spider crane and tight-access work',
  name='Spider Crane &amp; Tight Access', pre='Something else', img='cc-spider-indoor.jpg',
  alt='Cooper Crane mini spider crane working an indoor glass installation inside a Florida atrium',
  cap='Spider crane on an indoor glass install at MiamiCentral.',
  blurb='Trees, steel, signage, hot tubs, indoor glass. If you can rig it, we can lift it.',
  lede='When the job is inside a building, behind a gate, or in a courtyard a boom truck will never reach, the 2-ton spider crane goes where the big iron cannot.',
  intro='<p>The spider fits through a standard 36-inch gate, tracks across finished floors on rubber pads, and sets its own outriggers once it gets where it is going. <strong>We have run it inside atriums, through side yards and across plaza decks</strong>, including indoor glass work at MiamiCentral.</p><p>It is the machine that turns a "that cannot be craned" job into a normal Tuesday. Glass panels, HVAC in a mechanical room, statuary, equipment swaps in a basement plant room, hot tubs into a screened patio.</p>',
  h2a='Where the spider earns its money',
  pts=[('Indoor and atrium work','Glass, fixtures and equipment inside a finished building without tearing out a wall.'),
       ('Gated side yards','If a person can walk it, the spider can usually track it.'),
       ('Finished surfaces','Rubber tracks and spread pads instead of a 30,000 lb truck on your pavers.'),
       ('Elevated decks and plazas','Where load ratings rule out anything bigger.')],
  h2b='And everything else on the odd list',
  outro='<p>Trees, structural steel, signage, hot tubs, safes, statuary, aquariums, equipment swaps. If you can rig it, we can usually lift it, and if we genuinely cannot we will tell you that on the phone instead of billing you for a look.</p><p>Send a photo of the access route with your call. Nine times out of ten that single picture answers every question we would otherwise have to ask.</p>',
  spec=[('Machine','2-ton mini spider crane'),('Minimum gate width','36 inches'),('Surfaces','Rubber tracks, spread pads'),('Also on both','Boom trucks up to 40 ton')],
  kw='mini spider crane rental, indoor crane, tight access crane, glass installation crane'),
]

# ---------------------------------------------------------------- areas
# Every local read below is written from real characteristics of the place.
AREAS = [
 dict(slug='broward-county', name='Broward County', kind='county', county='Broward',
  drive='This is home. The yard sits in West Park, so most of Broward is inside a 30-minute run.',
  local='<p>Broward is our home county and the one we know street by street. The yard is in <strong>West Park</strong>, which puts Hollywood, Pembroke Pines, Miramar and Fort Lauderdale all inside a short run, and Coral Springs or Deerfield at the far end of an easy morning.</p><p>The building stock is split. South and central Broward is full of 1960s and 70s single-family homes with flat or low-slope roofs, carports and narrow side yards, which is where the spider crane and the 17-ton boom truck do most of their work. Downtown Fort Lauderdale and the beach strip are a different job entirely: mid-rise and high-rise decks, valet loading zones and a lot of coordination with building management.</p><p>Because we are based here, Broward jobs are the ones we can most often slot in same-week, and the ones where an urgent morning call has the best chance of getting a yes.</p>',
  cities=['Fort Lauderdale','Hollywood','Pembroke Pines','Pompano Beach','Coral Springs','Miramar','Davie','Plantation','Sunrise','Deerfield Beach']),

 dict(slug='miami-dade-county', name='Miami-Dade County', kind='county', county='Miami-Dade',
  drive='Roughly 20 to 45 minutes south of the yard depending on how far into the county you are.',
  local='<p>Miami-Dade is the densest part of our service area and the one that takes the most planning. <strong>Access is almost always the constraint, not capacity.</strong> Downtown, Brickell and the beach mean one-way streets, loading-zone permits, valet ramps and buildings that want a certificate of insurance before the outriggers come down.</p><p>Head inland and the job changes completely. Hialeah, Doral and Medley are warehouse and light-industrial country, where the lots are open, the picks are heavier and a 35-ton or 40-ton machine can actually stretch its legs. South Dade toward Homestead is single-family and agricultural, with long driveways and plenty of room to set up.</p><p>We ask more questions about Miami-Dade jobs than anywhere else, and it is not busywork. Knowing about the alley, the power line and the building manager before we leave the yard is the difference between a two-hour lift and a wasted trip.</p>',
  cities=['Miami','Miami Beach','Hialeah','Coral Gables','Doral','Aventura','North Miami','Homestead','Kendall','South Miami']),

 dict(slug='palm-beach-county', name='Palm Beach County', kind='county', county='Palm Beach',
  drive='The north end of our range. Boca is roughly 35 minutes; West Palm Beach is closer to an hour.',
  local='<p>Palm Beach County is the top of our territory and we plan it accordingly. <strong>The drive is real</strong>, so we would rather book Palm Beach work with a little notice and run it as a proper block than squeeze it into the back half of a Broward day.</p><p>South county, Boca Raton and Delray, is gated-community territory: HOA delivery windows, guard-gate paperwork, mature tree canopy that limits where a boom can swing, and pavers nobody wants an outrigger pad to crack. North into West Palm Beach you get a downtown core with real high-rise work around Clematis and Rosemary, plus older neighbourhoods like Northwood full of bungalows with tight side yards.</p><p>If you are coordinating several units across a Palm Beach property or an HOA, tell us on the first call. Batching those into one visit is usually cheaper for you than three separate trips up the coast.</p>',
  cities=['West Palm Beach','Boca Raton','Delray Beach','Boynton Beach','Jupiter','Wellington','Palm Beach Gardens','Lake Worth']),

 dict(slug='miami', name='Miami', kind='city', county='Miami-Dade',
  drive='About 25 to 35 minutes south of the West Park yard.',
  local='<p>Miami jobs are rarely about weight. They are about <strong>getting a truck to the building and getting the boom over it</strong>. Downtown and Brickell mean one-way grids, bus lanes, valet ramps and buildings whose management wants insurance paperwork and a scheduled window before anything rolls in.</p><p>Rooftop mechanical decks on mid and high-rise buildings are the common ask, and reach usually decides the machine long before tonnage does. On the tighter jobs, a courtyard, an interior atrium, a plaza deck with a load rating, the 2-ton spider crane goes in where nothing on wheels will fit. We ran it inside MiamiCentral for indoor glass work, which is about as tight as this city gets.</p><p>Give us the street address and a photo of where the truck would sit. In Miami that one picture answers most of what we would otherwise spend a phone call asking.</p>',
  cities=['Brickell','Downtown Miami','Little Havana','Wynwood','Coconut Grove','Edgewater']),

 dict(slug='fort-lauderdale', name='Fort Lauderdale', kind='city', county='Broward',
  drive='Roughly 20 minutes north of the yard.',
  local='<p>Fort Lauderdale is close enough that we can often get there the same day, and varied enough that no two jobs look alike. <strong>Downtown and Las Olas</strong> are mid and high-rise work with loading-zone coordination, while a few blocks away Victoria Park and Rio Vista are narrow historic streets with big shade trees and driveways a boom truck has to be threaded into.</p><p>The waterfront adds its own category. This is a marine city, and we get asked for lifts over seawalls, onto docks and around canal-front properties where the crane sets up on one side of a very expensive piece of landscaping and reaches over it.</p><p>Beach-side condo work is mostly AC and generator sets on decks, and it almost always needs a booked window with building management. Tell us the building name when you call; odds are decent we have already worked there.</p>',
  cities=['Las Olas','Victoria Park','Rio Vista','Coral Ridge','Harbor Beach']),

 dict(slug='west-palm-beach', name='West Palm Beach', kind='city', county='Palm Beach',
  drive='Closer to an hour from the yard, so we like a little notice.',
  local='<p>West Palm Beach is the far north end of our range and the drive is honest work, so we would rather schedule it properly than promise you a squeeze-in. <strong>Give us a day or two and you get a full, unhurried window</strong> instead of a crew watching the clock for the run home.</p><p>The downtown core around Clematis Street and Rosemary Avenue has genuine high-rise work: rooftop mechanical, generator sets on structural decks, and picks that need reach more than tonnage. Older neighbourhoods like Northwood and Flamingo Park are the opposite problem, 1920s and 30s bungalows on small lots with tight side yards, mature trees and driveways that were never built with a boom truck in mind.</p><p>If you have several units or several properties up here, batch them. One trip covering four addresses is materially cheaper for you than four trips, and we will help you sequence it.</p>',
  cities=['Downtown West Palm Beach','Northwood','Flamingo Park','El Cid','Clematis']),

 dict(slug='hollywood', name='Hollywood', kind='city', county='Broward',
  drive='About 10 minutes. This is the closest city to our yard.',
  local='<p>Hollywood is effectively our back yard. The West Park yard sits right on its edge, which makes this <strong>the easiest place in South Florida for us to say yes to a short-notice job</strong>. If something goes down on a Tuesday morning in Hollywood, we can usually do something about it that week.</p><p>Most of the housing stock is post-war single-family with flat and low-slope roofs, carports, and the narrow side yards that come with lots platted in the 1950s. That is bread-and-butter AC change-out and tarp-lift work, and it is where the 17-ton boom truck spends much of its life.</p><p>East toward the beach the job shifts to mid-rise condo buildings along the Broadwalk, where the work is rooftop mechanical and generator sets and the real task is booking a window with the association. West of I-95 the lots open up and setup gets simple again.</p>',
  cities=['Hollywood Beach','Emerald Hills','Hollywood Lakes','West Hollywood']),

 dict(slug='boca-raton', name='Boca Raton', kind='city', county='Palm Beach',
  drive='Roughly 35 minutes up the coast from the yard.',
  local='<p>Boca Raton is gated-community country, and that shapes almost every job here. <strong>Expect a guard gate, a certificate of insurance and a delivery window</strong>, and expect the association to care a great deal about what your outrigger pads are sitting on. We bring spread pads as a matter of course, because nobody wants to explain a cracked paver driveway.</p><p>The tree canopy is the other Boca constraint. A lot of these neighbourhoods have mature ficus and oak over the driveway, which limits where a boom can swing far more than the weight of whatever is on the hook. On the tightest properties the 2-ton spider crane tracks through a side gate and does the job from inside the yard.</p><p>Along the coast and around downtown there is genuine mid-rise work, rooftop mechanical and generator sets, and those are scheduled jobs with building management rather than drive-up work. Tell us the community or building name when you call and we will tell you what paperwork to expect.</p>',
  cities=['Downtown Boca','East Boca','Boca West','Mizner Park']),
]

SVC_BY = {s['slug']: s for s in SERVICES}
AREA_BY = {a['slug']: a for a in AREAS}

# ---------------------------------------------------------------- shared chrome
def nav_block():
    return """<nav class="site-nav" id="siteNav">
  <div class="nav-inner">
    <a href="%(p)s" class="nav-logo" aria-label="Cooper Crane home">
      <img class="badge" src="%(p)sassets/logo-badge.png" alt="" width="512" height="512">
      <img class="sign" src="%(p)sassets/logo-wordmark.png" alt="Cooper Crane" width="2061" height="428">
    </a>
    <ul class="nav-links">
      <li><a href="%(p)s#fleet">The Fleet</a></li>
      <li><a href="%(p)s#lift">What We Lift</a></li>
      <li><a href="%(p)sservice-areas/">Service Areas</a></li>
      <li><a href="%(p)s#how">How It Works</a></li>
      <li><a href="%(p)s#faq">FAQ</a></li>
    </ul>
    <div class="nav-right">
      <a href="tel:%(ph)s" class="nav-phone" data-call>%(phd)s</a>
      <a href="#qq" class="btn btn-sm">Get a Lift Quote</a>
    </div>
    <div class="mobile-actions">
      <a href="tel:%(ph)s" class="mobile-call" aria-label="Call Cooper Crane" data-call>
        <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.6 21 3 13.4 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.2.2 2.4.6 3.6.1.3 0 .7-.2 1l-2.3 2.2z"/></svg>
      </a>
      <button class="hamburger" id="hamburger" aria-label="Open menu" aria-controls="navDrawer" aria-expanded="false"><span></span><span></span><span></span></button>
    </div>
  </div>
</nav>

<div class="nav-overlay" id="navOverlay"></div>
<aside class="nav-drawer" id="navDrawer" aria-hidden="true">
  <div class="drawer-header">
    <img class="sign" src="%(p)sassets/logo-wordmark.png" alt="Cooper Crane" width="2061" height="428">
    <button class="drawer-close" id="drawerClose" aria-label="Close menu">&times;</button>
  </div>
  <nav class="drawer-links" aria-label="Mobile navigation">
    <a href="%(p)s">Home</a>
    <a href="%(p)s#fleet">The Fleet</a>
    <a href="%(p)s#lift">What We Lift</a>
    <a href="%(p)sservice-areas/">Service Areas</a>
    <a href="%(p)s#how">How It Works</a>
    <a href="%(p)s#work">Recent Lifts</a>
    <a href="%(p)s#faq">FAQ</a>
  </nav>
  <div class="drawer-footer">
    <a href="tel:%(ph)s" class="drawer-phone" data-call>
      <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.6 21 3 13.4 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.2.2 2.4.6 3.6.1.3 0 .7-.2 1l-2.3 2.2z"/></svg>
      %(phd)s
    </a>
    <a href="#qq" class="btn drawer-cta">Get a Lift Quote</a>
  </div>
</aside>""" % dict(p=PRE, ph=PHONE_H, phd=PHONE_D)

def footer_block():
    svc = ''.join('\n        <li><a href="%sservices/%s/">%s</a></li>' % (PRE, s['slug'], s['nav']) for s in SERVICES)
    ar = ''.join('\n        <li><a href="%sservice-areas/%s/">%s</a></li>' % (PRE, a['slug'], a['name']) for a in AREAS[:6])
    return """<footer>
  <div class="footer-inner">
    <div class="footer-brand">
      <img class="sign" src="%(p)sassets/logo-wordmark.png" alt="Cooper Crane" width="2061" height="428">
      <p class="tag">Southeast Florida Crane Service</p>
      <p>Certified-operator crane and boom truck service across Palm Beach, Broward and Miami-Dade, from a 2-ton mini spider crane to a 40-ton mobile crane.</p>
      <address>
        <a href="tel:%(ph)s" class="big" data-call>%(phd)s</a>
        <a href="mailto:%(em)s">%(em)s</a>
        <span>West Park, FL. Serving the Atlantic coast, West Palm Beach to South Miami.</span>
      </address>
      <div class="footer-social"><a href="https://www.facebook.com/CooperCraneFL" target="_blank" rel="noopener">Facebook</a></div>
    </div>
    <div class="footer-col">
      <h4>Explore</h4>
      <ul>
        <li><a href="%(p)s">Home</a></li>
        <li><a href="%(p)s#fleet">The Fleet</a></li>
        <li><a href="%(p)s#how">How Booking Works</a></li>
        <li><a href="%(p)s#why">Why Cooper</a></li>
        <li><a href="%(p)s#work">Recent Lifts</a></li>
        <li><a href="%(p)s#faq">FAQ</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <h4>Service Areas</h4>
      <ul>%(ar)s
        <li><a href="%(p)sservice-areas/">All service areas</a></li>
      </ul>
    </div>
    <div class="footer-col wide">
      <h4>What We Lift</h4>
      <ul>%(svc)s
      </ul>
    </div>
  </div>
  <div class="footer-bottom">
    <span>&copy; 2026 Cooper Crane LLC. All rights reserved.</span>
    <a class="built-by" href="https://crossdesigned.com" target="_blank" rel="noopener" aria-label="Website built by Cross Designs">
      <span>Built by</span>
      <img src="%(p)sassets/cross-designs.png" alt="Cross Designs">
    </a>
  </div>
</footer>""" % dict(p=PRE, ph=PHONE_H, phd=PHONE_D, em=EMAIL, svc=svc, ar=ar)

def qq_form(preselect):
    tiles = [('Rooftop AC unit','Rooftop AC unit','Condenser or air handler onto a curb'),
             ('Trusses or roofing material','Trusses or roofing','Truss packages, tile, shingle bundles'),
             ('Generator','Generator','Standby set onto a pad or roof'),
             ('Pest-control tarps','Pest-control tarps','Fumigation tenting over the roofline'),
             ('Something else','Something else','Steel, trees, hot tubs, tight access, not sure')]
    tl = ''.join('\n            <label class="qq-tile"><input type="radio" name="load" value="%s"><span><b>%s</b><em>%s</em></span></label>' % t for t in tiles)
    return """    <form class="qq" id="qq" novalidate data-preselect="%s">
      <p class="qq-hp"><label>Leave this empty <input type="text" name="company" tabindex="-1" autocomplete="off"></label></p>
      <div class="qq-top">
        <div class="qq-tag"><b>Lift Ticket</b><i id="qqCount">Step 1 / 3</i></div>
        <p>Three questions. We call you back with a number.</p>
        <div class="qq-bars" aria-hidden="true"><i class="on"></i><i></i><i></i></div>
      </div>
      <div class="qq-body">
        <div class="qq-sel" id="qqSel">Lifting: <b id="qqSelVal"></b><button type="button" id="qqChange">Change</button></div>
        <div class="qq-step on" data-step="1">
          <div class="qq-tiles" role="radiogroup" aria-label="What needs lifting">%s
          </div>
          <div class="qq-err" id="qqE1">Tap the closest one. We sort the details on the call.</div>
        </div>
        <div class="qq-step" data-step="2">
          <div class="qq-field">
            <label for="qq-where">Where is the job?</label>
            <input type="text" id="qq-where" name="where" placeholder="City or job site" autocomplete="address-level2">
            <div class="qq-msg">A city is enough to price the drive from our Broward yard.</div>
          </div>
          <div class="qq-field">
            <label for="qq-reach">How high and how heavy? <span class="qq-opt">optional</span></label>
            <input type="text" id="qq-reach" name="reach" placeholder="e.g. 600 lb, two stories, tight side yard">
          </div>
          <div class="qq-err" id="qqE2">Give us a city so we can price the drive.</div>
          <div class="qq-nav"><button type="button" class="qq-back">Back</button><button type="button" class="btn qq-next">Next</button></div>
        </div>
        <div class="qq-step" data-step="3">
          <div class="qq-field"><label for="qq-name">Name or business</label><input type="text" id="qq-name" name="name" placeholder="Jane Contractor" autocomplete="name"></div>
          <div class="qq-field"><label for="qq-phone">Phone</label><input type="tel" id="qq-phone" name="phone" placeholder="(555) 123-4567" autocomplete="tel"></div>
          <div class="qq-field"><label for="qq-email">Email <span class="qq-opt">optional</span></label><input type="email" id="qq-email" name="email" placeholder="you@email.com" autocomplete="email"></div>
          <div class="qq-err" id="qqE3">We need a name and a number to call you back.</div>
          <div class="qq-nav"><button type="button" class="qq-back">Back</button><button type="submit" class="btn">Send It</button></div>
        </div>
        <div class="qq-done" id="qqDone" role="status">
          <b>Sent. Talk shortly.</b>
          <p>Your email app opened with the details filled in. Hit send and we will call you back with a number.</p>
          <a href="tel:%s" class="btn" data-call>Or call now: %s</a>
        </div>
      </div>
    </form>""" % (preselect, tl, PHONE_H, PHONE_D)

JS = """<script src="%sassets/site.js?v=9" defer></script>""" % PRE

def head(title, desc, kw, url, extra_ld=''):
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>%(title)s</title>
<meta name="description" content="%(desc)s">
<meta name="keywords" content="%(kw)s">
<meta name="author" content="Cooper Crane LLC">
<meta name="robots" content="index, follow">
<meta name="geo.region" content="US-FL">
<meta name="geo.placename" content="West Park, Florida">
<meta name="geo.position" content="25.9837;-80.1820">
<meta name="ICBM" content="25.9837, -80.1820">
<link rel="canonical" href="%(url)s">
<meta property="og:title" content="%(title)s">
<meta property="og:description" content="%(desc)s">
<meta property="og:type" content="website">
<meta property="og:url" content="%(url)s">
<meta property="og:site_name" content="Cooper Crane LLC">
<meta property="og:locale" content="en_US">
<meta property="og:image" content="%(base)sassets/og-card.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Cooper Crane LLC. Crane and boom truck service, West Palm Beach to South Miami. (954) 445-6186.">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="%(title)s">
<meta name="twitter:description" content="%(desc)s">
<meta name="twitter:image" content="%(base)sassets/og-card.png">
<link rel="icon" type="image/png" href="%(p)sassets/favicon.png">
<link rel="apple-touch-icon" href="%(p)sassets/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Big+Shoulders:opsz,wght@10..72,600..800&family=Public+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="%(p)sassets/site.css?v=9">
%(ld)s
</head>
<body>
""" % dict(title=title, desc=desc, kw=kw, url=url, base=BASE, p=PRE, ld=extra_ld)

def ld(obj):
    return '<script type="application/ld+json">\n%s\n</script>' % json.dumps(obj, indent=2)

def biz():
    return {"@type":"LocalBusiness","name":"Cooper Crane LLC","@id":BASE+"#business",
            "telephone":"+1-954-445-6186","email":EMAIL,
            "address":{"@type":"PostalAddress","addressLocality":"West Park","addressRegion":"FL","postalCode":"33023","addressCountry":"US"}}

def crumbs_ld(items):
    return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":i+1,"name":n,"item":u} for i,(n,u) in enumerate(items)]}

def faq_ld(faqs):
    return {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]}

def faq_html(faqs):
    return ''.join('\n        <div class="acc-item"><button class="acc-header" aria-expanded="false">%s <span class="pm" aria-hidden="true">+</span></button><div class="acc-content"><div class="acc-text">%s</div></div></div>' % (q,a) for q,a in faqs)

def quote_band(preselect, headline, copy):
    return """<section class="sp-quote">
  <div class="sp-quote-inner">
    <div class="sp-quote-copy">
      <div class="rule" aria-hidden="true"></div>
      <h2 class="headline">%s</h2>
      %s
      <span class="alt-call">Rather talk it out? <a href="tel:%s" data-call>%s</a></span>
    </div>
%s
  </div>
</section>""" % (headline, copy, PHONE_H, PHONE_D, qq_form(preselect))

def write(path, htmlstr):
    assert '\u2014' not in htmlstr, 'em dash in ' + path
    # templates are authored at depth 2 (PRE = '../../'); retarget for shallower pages
    depth = path.count('/')
    if depth != 2:
        htmlstr = htmlstr.replace(PRE, '../' * depth if depth else './')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'w', encoding='utf-8').write(htmlstr)

# ---------------------------------------------------------------- builders
def build_service(s):
    url = BASE + 'services/' + s['slug'] + '/'
    faqs = [('Do you provide the crane operator?','Yes. Every Cooper Crane machine comes with a certified, experienced operator who handles the rigging and signaling. There is no separate operator to hire.'),
            ('Which areas do you cover?','Every job from West Palm Beach to South Miami: Palm Beach, Broward and Miami-Dade counties, out of one Broward yard on one number, (954) 445-6186.'),
            ('How do I know what size crane I need?','Tell us how heavy the load is, how high it has to go and how far the crane has to reach, plus any access limits. We spec the right machine on the call, and we pick the smallest one that safely does the job.'),
            ('How far ahead should I book?','Earlier is better for scheduling, but we keep multiple machines in the yard and will always try to work in urgent and same-week lifts.')]
    svc_ld = {"@context":"https://schema.org","@type":"Service","name":s['name'].replace('&amp;','&'),
      "serviceType":s['name'].replace('&amp;','&'),"description":s['blurb'],"url":url,"provider":biz(),
      "areaServed":[{"@type":"AdministrativeArea","name":n} for n in ["Palm Beach County, FL","Broward County, FL","Miami-Dade County, FL"]]}
    lds = ld(svc_ld) + '\n' + ld(crumbs_ld([("Home",BASE),("What We Lift",BASE+"#lift"),(s['name'].replace('&amp;','&'),url)])) + '\n' + ld(faq_ld(faqs))

    pts = ''.join('\n        <li><span class="mk" aria-hidden="true">&#9632;</span><div><b>%s.</b> %s</div></li>' % t for t in s['pts'])
    spec = ''.join('\n          <div class="row"><dt>%s</dt><dd>%s</dd></div>' % t for t in s['spec'])
    # anchor matrix: this service in every area
    areamx = ''.join('\n      <a class="mx-chip" href="%sservices/%s-in-%s/">%s in %s</a>' % (PRE, s['slug'], a['slug'], s['nav'], a['name']) for a in AREAS)
    others = ''.join('\n      <a class="other-card" href="%sservices/%s/"><b>%s</b><span>View &rarr;</span></a>' % (PRE, o['slug'], o['nav']) for o in SERVICES if o['slug'] != s['slug'])

    return head(s['name'].replace('&amp;','&') + ', South Florida | Cooper Crane',
                s['blurb'] + ' Palm Beach, Broward and Miami-Dade. Call (954) 445-6186.',
                s['kw'], url, lds) + """%(nav)s

<header class="sp-hero">
  <div class="sp-hero-bg" style="background-image:url('%(p)sassets/%(img)s')" aria-hidden="true"></div>
  <div class="sp-hero-inner">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="%(p)s">Home</a><span>&rsaquo;</span><a href="%(p)s#lift">What We Lift</a><span>&rsaquo;</span>%(name)s</nav>
    <h1>%(name)s</h1>
    <p class="lede">%(lede)s</p>
    <div class="sp-ctas">
      <a href="tel:%(ph)s" class="btn" data-call>Call %(phd)s</a>
      <a href="#qq" class="btn btn-ghost">Get a Lift Quote</a>
    </div>
  </div>
</header>

<section class="sp-body">
  <div class="sp-inner">
    <div class="sp-main">
      <div class="rule" aria-hidden="true"></div>
      %(intro)s
      <figure class="sp-photo"><img src="%(p)sassets/%(img)s" alt="%(alt)s" loading="lazy"><figcaption>%(cap)s</figcaption></figure>
      <h2 class="mt">%(h2a)s</h2>
      <ul class="sp-list">%(pts)s
      </ul>
      <h2 class="mt">%(h2b)s</h2>
      %(outro)s
    </div>
    <aside class="sp-aside">
      <div class="sp-card">
        <b>Talk to the yard</b>
        <p>Tell us the weight, the height and the reach. We spec the machine and quote it on the call.</p>
        <a href="tel:%(ph)s" class="big-phone" data-call>%(phd)s</a>
        <a href="tel:%(ph)s" class="btn" data-call>Reach Out</a>
      </div>
      <div class="sp-spec"><b>Quick spec</b><dl>%(spec)s
        </dl>
      </div>
    </aside>
  </div>
</section>

%(quote)s

<section class="mx alt">
  <div class="mx-inner">
    <div class="rule" aria-hidden="true"></div>
    <h2 class="headline">%(nav_name)s, Where You Need It</h2>
    <p>Same crane, same operator, wherever the job sits between West Palm Beach and South Miami.</p>
    <div class="mx-grid">%(areamx)s
    </div>
  </div>
</section>

<section class="faq" id="faq">
  <div class="faq-inner">
    <div class="faq-intro">
      <div class="rule" aria-hidden="true"></div>
      <h2 class="headline">Questions We Get on This One</h2>
      <p>Still unsure what you need? A two-minute call sorts it out.</p>
      <a href="tel:%(ph)s" class="btn" data-call>Call %(phd)s</a>
    </div>
    <div class="accordion">%(faqs)s
    </div>
  </div>
</section>

<section class="sp-other">
  <div class="mx-inner">
    <div class="rule" aria-hidden="true"></div>
    <h2 class="headline">The Other Lifts We Run</h2>
  </div>
  <div class="other-grid">%(others)s
  </div>
</section>

%(footer)s
%(js)s
</body>
</html>
""" % dict(nav=nav_block(), p=PRE, img=s['img'], name=s['name'], lede=s['lede'], ph=PHONE_H, phd=PHONE_D,
           intro=s['intro'], alt=s['alt'], cap=s['cap'], h2a=s['h2a'], pts=pts, h2b=s['h2b'], outro=s['outro'],
           spec=spec, quote=quote_band(s['pre'],'Price This Lift','<p>Already on the right page, so we have filled in the first question. <strong>Change it if your job is something else</strong> and send it either way.</p><p>Three questions, then we call you back with a real number.</p>'),
           nav_name=s['nav'], areamx=areamx, faqs=faq_html(faqs), others=others, footer=footer_block(), js=JS)


def build_area(a):
    url = BASE + 'service-areas/' + a['slug'] + '/'
    faqs = [('Do you charge extra to come to %s?' % a['name'],'The drive is one of the three things that move the price, along with the machine your load needs and how long we are on site. %s We tell you the number before anything is booked.' % a['drive']),
            ('How fast can you get to %s?' % a['name'],'%s Urgent and same-week jobs are worth a phone call rather than a form, and we will tell you honestly what we can do.' % a['drive']),
            ('Do you provide the operator?','Yes. Every crane comes with a certified Cooper Crane operator who handles rigging and signaling. We run the machine; you point at what needs to move.')]
    area_ld = {"@context":"https://schema.org","@type":"LocalBusiness","name":"Cooper Crane LLC","@id":BASE+"#business",
      "url":url,"telephone":"+1-954-445-6186","email":EMAIL,"priceRange":"$$",
      "image":BASE+"assets/og-card.png",
      "address":{"@type":"PostalAddress","addressLocality":"West Park","addressRegion":"FL","postalCode":"33023","addressCountry":"US"},
      "geo":{"@type":"GeoCoordinates","latitude":"25.9837","longitude":"-80.1820"},
      "areaServed":{"@type":"AdministrativeArea" if a['kind']=='county' else "City","name":a['name']},
      "aggregateRating":{"@type":"AggregateRating","ratingValue":"4.0","reviewCount":"20"}}
    lds = ld(area_ld) + '\n' + ld(crumbs_ld([("Home",BASE),("Service Areas",BASE+"service-areas/"),(a['name'],url)])) + '\n' + ld(faq_ld(faqs))

    svc_cards = ''.join("""
      <a class="mx-card" href="%sservices/%s-in-%s/">
        <span class="mx-no">%02d</span>
        <b>%s in %s</b>
        <em>%s</em>
        <span class="mx-go">See details &rarr;</span>
      </a>""" % (PRE, s['slug'], a['slug'], i+1, s['nav'], a['name'], s['blurb']) for i, s in enumerate(SERVICES))
    nearby = [x for x in AREAS if x['slug'] != a['slug'] and (x['county'] == a['county'] or x['kind'] != a['kind'])][:5]
    near = ''.join('\n      <a class="mx-chip" href="%sservice-areas/%s/">%s</a>' % (PRE, n['slug'], n['name']) for n in nearby)
    towns = ' &middot; '.join(a['cities'])

    return head('Crane Rental in %s | Cooper Crane' % a['name'],
                'Certified-operator crane and boom truck service in %s. 2 to 40 tons, AC units, trusses, roofing, generators. Call (954) 445-6186.' % a['name'],
                'crane rental %s, boom truck %s, crane service %s' % (a['name'].lower(), a['name'].lower(), a['name'].lower()),
                url, lds) + """%(nav)s

<header class="sp-hero">
  <div class="sp-hero-bg" style="background-image:url('%(p)sassets/hero-fleet.jpg')" aria-hidden="true"></div>
  <div class="sp-hero-inner">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="%(p)s">Home</a><span>&rsaquo;</span><a href="%(p)sservice-areas/">Service Areas</a><span>&rsaquo;</span>%(name)s</nav>
    <h1>Crane Rental in %(name)s</h1>
    <p class="lede">%(drive)s Certified operator on every lift, from a 2-ton spider crane to a 40-ton mobile crane.</p>
    <div class="sp-ctas">
      <a href="tel:%(ph)s" class="btn" data-call>Call %(phd)s</a>
      <a href="#qq" class="btn btn-ghost">Get a Lift Quote</a>
    </div>
  </div>
</header>

<section class="sp-body">
  <div class="sp-inner">
    <div class="sp-main">
      <div class="rule" aria-hidden="true"></div>
      <h2>What lifting in %(name)s actually looks like</h2>
      %(local)s
    </div>
    <aside class="sp-aside">
      <div class="sp-card">
        <b>Talk to the yard</b>
        <p>Tell us the weight, the height and the reach. We spec the machine and quote it on the call.</p>
        <a href="tel:%(ph)s" class="big-phone" data-call>%(phd)s</a>
        <a href="tel:%(ph)s" class="btn" data-call>Reach Out</a>
      </div>
      <div class="sp-spec"><b>%(name)s at a glance</b><dl>
          <div class="row"><dt>From our yard</dt><dd>%(drive)s</dd></div>
          <div class="row"><dt>County</dt><dd>%(county)s</dd></div>
          <div class="row"><dt>Fleet available</dt><dd>2, 17, 35 and 40 ton</dd></div>
          <div class="row"><dt>Operator</dt><dd>Certified, included</dd></div>
        </dl>
      </div>
    </aside>
  </div>
</section>

<section class="mx">
  <div class="mx-inner">
    <div class="rule" aria-hidden="true"></div>
    <h2 class="headline">What We Lift in %(name)s</h2>
    <p>Every service we run, priced and scheduled for %(name)s specifically.</p>
    <div class="mx-cards">%(cards)s
    </div>
  </div>
</section>

%(quote)s

<section class="mx alt">
  <div class="mx-inner">
    <div class="rule" aria-hidden="true"></div>
    <h2 class="headline">Also Covered Nearby</h2>
    <p class="mx-towns">Inside %(name)s we regularly work %(towns)s.</p>
    <div class="mx-grid">%(near)s
      <a class="mx-chip" href="%(p)sservice-areas/">All service areas</a>
    </div>
  </div>
</section>

<section class="faq" id="faq">
  <div class="faq-inner">
    <div class="faq-intro">
      <div class="rule" aria-hidden="true"></div>
      <h2 class="headline">%(name)s Questions</h2>
      <p>Still unsure what you need? A two-minute call sorts it out.</p>
      <a href="tel:%(ph)s" class="btn" data-call>Call %(phd)s</a>
    </div>
    <div class="accordion">%(faqs)s
    </div>
  </div>
</section>

%(footer)s
%(js)s
</body>
</html>
""" % dict(nav=nav_block(), p=PRE, name=a['name'], drive=a['drive'], local=a['local'], ph=PHONE_H, phd=PHONE_D,
           county=a['county'], cards=svc_cards, near=near, towns=towns, faqs=faq_html(faqs),
           quote=quote_band('', 'Price a Lift in %s' % a['name'], '<p>Tell us what needs lifting and where it sits in %s. <strong>Three questions</strong> and we call you back with a real number.</p>' % a['name']),
           footer=footer_block(), js=JS)


def build_combo(s, a):
    slug = '%s-in-%s' % (s['slug'], a['slug'])
    url = BASE + 'services/' + slug + '/'
    title = '%s in %s | Cooper Crane' % (s['name'].replace('&amp;','&'), a['name'])
    desc = '%s in %s. %s Certified operator, 2 to 40 tons. Call (954) 445-6186.' % (s['name'].replace('&amp;','&'), a['name'], s['blurb'])
    faqs = [('Do you cover all of %s for %s?' % (a['name'], s['short']),'Yes. %s We run %s across the whole area with the same fleet and the same certified operators.' % (a['drive'], s['short'])),
            ('What do you need to know before quoting?','How heavy the load is, how high it has to go, how far the crane has to reach, and anything tight about the access. That is usually enough to spec the machine and price it on the call.'),
            ('How fast can you get to %s?' % a['name'],'%s Urgent work is worth a phone call rather than a form.' % a['drive'])]
    svc_ld = {"@context":"https://schema.org","@type":"Service","name":'%s in %s' % (s['name'].replace('&amp;','&'), a['name']),
      "serviceType":s['name'].replace('&amp;','&'),"description":desc,"url":url,"provider":biz(),
      "areaServed":{"@type":"AdministrativeArea" if a['kind']=='county' else "City","name":a['name']}}
    lds = ld(svc_ld) + '\n' + ld(crumbs_ld([("Home",BASE),("What We Lift",BASE+"#lift"),(s['name'].replace('&amp;','&'),BASE+'services/'+s['slug']+'/'),('%s in %s' % (s['nav'], a['name']),url)])) + '\n' + ld(faq_ld(faqs))

    pts = ''.join('\n        <li><span class="mk" aria-hidden="true">&#9632;</span><div><b>%s.</b> %s</div></li>' % t for t in s['pts'])
    sib = ''.join('\n      <a class="mx-chip" href="%sservices/%s-in-%s/">%s in %s</a>' % (PRE, o['slug'], a['slug'], o['nav'], a['name']) for o in SERVICES if o['slug'] != s['slug'])
    elsewhere = ''.join('\n      <a class="mx-chip" href="%sservices/%s-in-%s/">%s in %s</a>' % (PRE, s['slug'], x['slug'], s['nav'], x['name']) for x in AREAS if x['slug'] != a['slug'])

    return head(title, desc, '%s %s, %s' % (s['nav'].lower(), a['name'].lower(), s['kw']), url, lds) + """%(nav)s

<header class="sp-hero">
  <div class="sp-hero-bg" style="background-image:url('%(p)sassets/%(img)s')" aria-hidden="true"></div>
  <div class="sp-hero-inner">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="%(p)s">Home</a><span>&rsaquo;</span><a href="%(p)sservices/%(sslug)s/">%(sname)s</a><span>&rsaquo;</span>%(aname)s</nav>
    <h1>%(sname)s in %(aname)s</h1>
    <p class="lede">%(lede)s</p>
    <div class="sp-ctas">
      <a href="tel:%(ph)s" class="btn" data-call>Call %(phd)s</a>
      <a href="#qq" class="btn btn-ghost">Get a Lift Quote</a>
    </div>
  </div>
</header>

<section class="sp-body">
  <div class="sp-inner">
    <div class="sp-main">
      <div class="rule" aria-hidden="true"></div>
      <h2>%(sname)s, %(aname)s</h2>
      <p>%(drive)s We bring the same fleet and the same certified operators to %(aname)s that we bring anywhere else between West Palm Beach and South Miami.</p>
      %(intro)s
      <figure class="sp-photo"><img src="%(p)sassets/%(img)s" alt="%(alt)s" loading="lazy"><figcaption>%(cap)s</figcaption></figure>
      <h2 class="mt">Working in %(aname)s</h2>
      %(local)s
      <h2 class="mt">%(h2a)s</h2>
      <ul class="sp-list">%(pts)s
      </ul>
      <p class="sp-more">Want the full rundown on this service? <a href="%(p)sservices/%(sslug)s/">Read the %(sname)s page</a>, or see <a href="%(p)sservice-areas/%(aslug)s/">everything we lift in %(aname)s</a>.</p>
    </div>
    <aside class="sp-aside">
      <div class="sp-card">
        <b>Talk to the yard</b>
        <p>Tell us the weight, the height and the reach. We spec the machine and quote it on the call.</p>
        <a href="tel:%(ph)s" class="big-phone" data-call>%(phd)s</a>
        <a href="tel:%(ph)s" class="btn" data-call>Reach Out</a>
      </div>
      <div class="sp-spec"><b>Quick spec</b><dl>%(spec)s
        </dl>
      </div>
    </aside>
  </div>
</section>

%(quote)s

<section class="mx alt">
  <div class="mx-inner">
    <div class="rule" aria-hidden="true"></div>
    <h2 class="headline">Other Lifts in %(aname)s</h2>
    <div class="mx-grid">%(sib)s
      <a class="mx-chip" href="%(p)sservice-areas/%(aslug)s/">All %(aname)s work</a>
    </div>
    <h2 class="headline mx-h2b">%(nav_name)s Elsewhere</h2>
    <div class="mx-grid">%(elsewhere)s
    </div>
  </div>
</section>

<section class="faq" id="faq">
  <div class="faq-inner">
    <div class="faq-intro">
      <div class="rule" aria-hidden="true"></div>
      <h2 class="headline">%(aname)s Questions</h2>
      <p>Still unsure what you need? A two-minute call sorts it out.</p>
      <a href="tel:%(ph)s" class="btn" data-call>Call %(phd)s</a>
    </div>
    <div class="accordion">%(faqs)s
    </div>
  </div>
</section>

%(footer)s
%(js)s
</body>
</html>
""" % dict(nav=nav_block(), p=PRE, img=s['img'], sslug=s['slug'], aslug=a['slug'],
           sname=s['name'], aname=a['name'], lede=s['lede'], ph=PHONE_H, phd=PHONE_D,
           drive=a['drive'], intro=s['intro'], alt=s['alt'], cap=s['cap'], local=a['local'],
           h2a=s['h2a'], pts=pts, spec=''.join('\n          <div class="row"><dt>%s</dt><dd>%s</dd></div>' % t for t in s['spec']),
           quote=quote_band(s['pre'], 'Price This %s Lift' % a['name'], '<p>We have filled in the first question for you. <strong>Change it if your job is something else.</strong></p><p>Three questions, then we call you back with a real number.</p>'),
           sib=sib, elsewhere=elsewhere, nav_name=s['nav'], faqs=faq_html(faqs), footer=footer_block(), js=JS)


def build_hub():
    url = BASE + 'service-areas/'
    counties = [a for a in AREAS if a['kind']=='county']
    cities = [a for a in AREAS if a['kind']=='city']
    def cards(lst):
        return ''.join("""
      <a class="mx-card" href="%sservice-areas/%s/">
        <b>Crane Rental in %s</b>
        <em>%s</em>
        <span class="mx-go">See details &rarr;</span>
      </a>""" % (PRE, a['slug'], a['name'], a['drive']) for a in lst)
    lds = ld(crumbs_ld([("Home",BASE),("Service Areas",url)]))
    return head('Crane Service Areas, West Palm Beach to South Miami | Cooper Crane',
                'Where Cooper Crane works: Palm Beach, Broward and Miami-Dade counties, plus Miami, Fort Lauderdale, West Palm Beach, Hollywood and Boca Raton. Call (954) 445-6186.',
                'crane service areas south florida, crane rental broward, crane rental miami dade, crane rental palm beach',
                url, lds) + """%(nav)s

<header class="sp-hero">
  <div class="sp-hero-bg" style="background-image:url('%(p)sassets/fleet-lineup.jpg')" aria-hidden="true"></div>
  <div class="sp-hero-inner">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="%(p)s">Home</a><span>&rsaquo;</span>Service Areas</nav>
    <h1>Every Job From West Palm Beach to South Miami</h1>
    <p class="lede">One yard in West Park, one number, three counties. Pick your area and see what a lift there actually involves.</p>
    <div class="sp-ctas">
      <a href="tel:%(ph)s" class="btn" data-call>Call %(phd)s</a>
      <a href="#qq" class="btn btn-ghost">Get a Lift Quote</a>
    </div>
  </div>
</header>

<section class="mx">
  <div class="mx-inner">
    <div class="rule" aria-hidden="true"></div>
    <h2 class="headline">By County</h2>
    <div class="mx-cards">%(counties)s
    </div>
    <h2 class="headline mx-h2b">By City</h2>
    <div class="mx-cards">%(cities)s
    </div>
    <p class="mx-towns">Do not see your town? We cover the whole Atlantic coast between West Palm Beach and South Miami. Call the yard and ask.</p>
  </div>
</section>

%(quote)s

%(footer)s
%(js)s
</body>
</html>
""" % dict(nav=nav_block(), p=PRE, ph=PHONE_H, phd=PHONE_D, counties=cards(counties), cities=cards(cities),
           quote=quote_band('', 'Price a Lift Anywhere We Run', '<p>Tell us what needs lifting and where it sits. <strong>Three questions</strong> and we call you back with a real number.</p>'),
           footer=footer_block(), js=JS)


# ---------------------------------------------------------------- run
if __name__ == '__main__':
    urls = [BASE]
    for s in SERVICES:
        write('services/%s/index.html' % s['slug'], build_service(s)); urls.append(BASE+'services/%s/' % s['slug'])
    write('service-areas/index.html', build_hub()); urls.append(BASE+'service-areas/')
    for a in AREAS:
        write('service-areas/%s/index.html' % a['slug'], build_area(a)); urls.append(BASE+'service-areas/%s/' % a['slug'])
    for s in SERVICES:
        for a in AREAS:
            slug = '%s-in-%s' % (s['slug'], a['slug'])
            write('services/%s/index.html' % slug, build_combo(s, a)); urls.append(BASE+'services/%s/' % slug)

    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for u in urls:
        pr = '1.0' if u == BASE else ('0.8' if u.count('/') <= 5 else '0.6')
        sm += '  <url><loc>%s</loc><lastmod>2026-08-10</lastmod><priority>%s</priority></url>\n' % (u, pr)
    sm += '</urlset>\n'
    open('sitemap.xml','w',encoding='utf-8').write(sm)
    print('pages:', len(urls), '(1 home + %d services + 1 hub + %d areas + %d combos)' % (len(SERVICES), len(AREAS), len(SERVICES)*len(AREAS)))
