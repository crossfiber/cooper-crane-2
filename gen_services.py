#!/usr/bin/env python3
"""Generate Cooper Crane service subpages from one template.
Nav/drawer/footer links are all prefixed ../ so anchors land on the homepage.
"""
import os, json

_idx = open('index.html', encoding='utf-8').read()
STYLE = _idx[_idx.index('<style>'):_idx.index('</style>') + len('</style>')]

TILES = [
 ('Rooftop AC unit', 'Rooftop AC unit', 'Condenser or air handler onto a curb'),
 ('Trusses or roofing material', 'Trusses or roofing', 'Truss packages, tile, shingle bundles'),
 ('Generator', 'Generator', 'Standby set onto a pad or roof'),
 ('Pest-control tarps', 'Pest-control tarps', 'Fumigation tenting over the roofline'),
 ('Something else', 'Something else', 'Steel, trees, hot tubs, tight access, not sure'),
]

def qq_form(preselect):
    tiles = ''.join(
      '\n            <label class="qq-tile"><input type="radio" name="load" value="%s"><span><b>%s</b><em>%s</em></span></label>' % t
      for t in TILES)
    return '''    <form class="qq" id="qq" novalidate data-preselect="%s">
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
            <input type="text" id="qq-where" name="where" placeholder="City or job site, e.g. Hollywood" autocomplete="address-level2">
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
          <div class="qq-field">
            <label for="qq-name">Name or business</label>
            <input type="text" id="qq-name" name="name" placeholder="Jane Contractor" autocomplete="name">
          </div>
          <div class="qq-field">
            <label for="qq-phone">Phone</label>
            <input type="tel" id="qq-phone" name="phone" placeholder="(555) 123-4567" autocomplete="tel">
          </div>
          <div class="qq-field">
            <label for="qq-email">Email <span class="qq-opt">optional</span></label>
            <input type="email" id="qq-email" name="email" placeholder="you@email.com" autocomplete="email">
          </div>
          <div class="qq-err" id="qqE3">We need a name and a number to call you back.</div>
          <div class="qq-nav"><button type="button" class="qq-back">Back</button><button type="submit" class="btn">Send It</button></div>
        </div>

        <div class="qq-done" id="qqDone" role="status">
          <b>Sent. Talk shortly.</b>
          <p>Your email app opened with the details filled in. Hit send and we will call you back with a number.</p>
          <a href="tel:+19544456186" class="btn" data-call>Or call now: (954) 445-6186</a>
        </div>
      </div>
    </form>''' % (preselect, tiles)

EXTRA_CSS = """
<style>
  /* ---- subpage-only additions ---- */
  .sp-hero { position: relative; background: var(--navy); color: var(--bone); padding: calc(var(--nav-h) + 54px) 30px 54px; overflow: hidden; }
  .sp-hero-bg { position: absolute; inset: 0; background-size: cover; background-position: center 50%; opacity: 0.28; }
  .sp-hero::after { content: ''; position: absolute; inset: 0; background: linear-gradient(96deg, rgba(13,21,36,0.95) 0%, rgba(13,21,36,0.78) 55%, rgba(16,25,43,0.55) 100%); }
  .sp-hero-inner { position: relative; z-index: 2; max-width: 1100px; margin: 0 auto; }
  .crumbs { font-size: 0.86rem; color: var(--bone-mute); margin-bottom: 16px; }
  .crumbs a { color: var(--bone); text-decoration: none; border-bottom: 1px solid rgba(244,243,238,0.35); }
  .crumbs a:hover { color: #fff; border-color: #fff; }
  .crumbs span { margin: 0 7px; opacity: 0.5; }
  .sp-hero h1 { font-size: clamp(2.4rem, 5.4vw, 4rem); color: var(--bone); line-height: 0.98; margin-bottom: 14px; }
  .sp-hero p.lede { font-size: 1.12rem; line-height: 1.6; color: var(--bone-mute); max-width: 620px; margin-bottom: 26px; }
  .sp-ctas { display: flex; gap: 12px; flex-wrap: wrap; }

  .sp-body { background: var(--porcelain); }
  .sp-inner { max-width: 1100px; margin: 0 auto; display: grid; grid-template-columns: 1.15fr 0.85fr; gap: 54px; align-items: start; }
  .sp-main h2 { font-size: clamp(1.7rem, 3vw, 2.3rem); color: var(--ink); margin: 0 0 14px; }
  .sp-main h2.mt { margin-top: 38px; }
  .sp-main p { font-size: 1.02rem; line-height: 1.7; color: var(--ink-soft); margin-bottom: 14px; }
  .sp-main p strong { color: var(--ink); font-weight: 600; }
  .sp-list { list-style: none; display: flex; flex-direction: column; gap: 0; margin: 6px 0 18px; }
  .sp-list li { display: flex; gap: 14px; align-items: flex-start; padding: 13px 0; border-top: 1px solid rgba(23,32,47,0.14); font-size: 0.99rem; color: var(--ink-soft); line-height: 1.55; }
  .sp-list li:last-child { border-bottom: 1px solid rgba(23,32,47,0.14); }
  .sp-list .mk { color: var(--red); font-size: 0.8rem; margin-top: 6px; flex-shrink: 0; }
  .sp-list b { color: var(--ink); font-weight: 600; }
  .sp-photo { border-radius: 6px; overflow: hidden; box-shadow: var(--shadow-md); margin: 24px 0 8px; }
  .sp-photo img { width: 100%; height: auto; display: block; }
  .sp-photo figcaption { background: var(--navy); color: var(--bone-mute); font-size: 0.84rem; padding: 10px 14px; }

  .sp-aside { position: sticky; top: calc(var(--nav-h) + 26px); display: flex; flex-direction: column; gap: 16px; }
  .sp-card { background: var(--navy); color: var(--bone); border-radius: 6px; padding: 26px 24px; border-left: 6px solid var(--red); }
  .sp-card b { font-family: 'Big Shoulders', sans-serif; font-weight: 800; font-size: 1.4rem; text-transform: uppercase; letter-spacing: 0.03em; display: block; line-height: 1.1; margin-bottom: 8px; }
  .sp-card p { font-size: 0.95rem; color: var(--bone-mute); line-height: 1.55; margin-bottom: 16px; }
  .sp-card .big-phone { font-family: 'Big Shoulders', sans-serif; font-weight: 800; font-size: 1.9rem; color: var(--bone); text-decoration: none; display: block; line-height: 1; margin-bottom: 12px; letter-spacing: 0.02em; }
  .sp-card .big-phone:hover { color: #fff; }
  .sp-card .btn { width: 100%; }
  .sp-spec { background: #fff; border: 1px solid var(--line); border-radius: 6px; padding: 22px 24px; }
  .sp-spec b { font-family: 'Big Shoulders', sans-serif; font-weight: 700; font-size: 1.12rem; letter-spacing: 0.05em; text-transform: uppercase; color: var(--ink); display: block; margin-bottom: 12px; }
  .sp-spec dl { display: flex; flex-direction: column; gap: 11px; margin: 0; }
  .sp-spec .row { display: block; border-bottom: 1px dashed rgba(23,32,47,0.16); padding-bottom: 10px; }
  .sp-spec .row:last-child { border-bottom: none; padding-bottom: 0; }
  .sp-spec dt { font-family: 'Big Shoulders', sans-serif; font-weight: 700; font-size: 0.82rem; letter-spacing: 0.13em; text-transform: uppercase; color: var(--ink-soft); margin: 0 0 2px; }
  .sp-spec dd { color: var(--ink); font-weight: 600; font-size: 0.97rem; line-height: 1.4; margin: 0; }

  /* on-page lift ticket band */
  .sp-quote { background: var(--navy); }
  .sp-quote-inner { max-width: 1100px; margin: 0 auto; display: grid; grid-template-columns: 1fr 0.92fr; gap: 54px; align-items: center; }
  .sp-quote-copy .headline { color: var(--bone); margin-bottom: 14px; }
  .sp-quote-copy p { font-size: 1.04rem; line-height: 1.65; color: var(--bone-mute); margin-bottom: 12px; }
  .sp-quote-copy p strong { color: var(--bone); font-weight: 600; }
  .sp-quote-copy .alt-call { display: inline-flex; align-items: baseline; gap: 10px; margin-top: 8px; font-size: 0.95rem; color: var(--bone-mute); }
  .sp-quote-copy .alt-call a { font-family: 'Big Shoulders', sans-serif; font-weight: 800; font-size: 1.5rem; color: var(--bone); text-decoration: none; letter-spacing: 0.02em; }
  .sp-quote-copy .alt-call a:hover { color: #fff; }
  @media (max-width: 1024px) { .sp-quote-inner { grid-template-columns: 1fr; gap: 28px; } }

  .sp-other { background: var(--porcelain-alt); }
  .other-grid { max-width: 1100px; margin: 0 auto; display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px; }
  .other-card { background: #fff; border: 1px solid var(--line); border-radius: 5px; padding: 18px 18px 16px; text-decoration: none; display: block; transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease; }
  .other-card:hover { transform: translateY(-3px); box-shadow: var(--shadow-sm); border-color: rgba(178,35,53,0.45); }
  .other-card b { font-family: 'Big Shoulders', sans-serif; font-weight: 700; font-size: 1.1rem; letter-spacing: 0.03em; text-transform: uppercase; color: var(--ink); display: block; line-height: 1.12; }
  .other-card span { font-size: 0.84rem; color: var(--red); font-weight: 600; }

  @media (max-width: 1024px) {
    .sp-inner { grid-template-columns: 1fr; gap: 32px; }
    .sp-aside { position: static; flex-direction: row; flex-wrap: wrap; }
    .sp-card, .sp-spec { flex: 1 1 300px; }
    .other-grid { grid-template-columns: repeat(3, 1fr); }
  }
  @media (max-width: 768px) {
    .sp-hero { padding: calc(var(--nav-h-sm) + 34px) 20px 36px; }
    .sp-hero h1 { font-size: 2.3rem; }
    .sp-hero p.lede { font-size: 1rem; }
    .sp-ctas { flex-direction: column; align-items: stretch; }
    .sp-ctas .btn { width: 100%; }
    .sp-aside { flex-direction: column; }
    .other-grid { grid-template-columns: 1fr 1fr; gap: 10px; }
    .sp-main h2.mt { margin-top: 28px; }
  }
</style>"""

BASE = 'https://crossfiber.github.io/cooper-crane-2/'
PHONE_D = '(954) 445-6186'
PHONE_H = '+19544456186'

SERVICES = [
 dict(slug='ac-unit-lifts', pre='Rooftop AC unit', nav='AC Units',
  name='Rooftop AC Unit Lifts',
  h1='Rooftop AC Unit Lifts, West Palm to South Miami',
  title='Rooftop AC Unit Crane Lifts, Broward &amp; Miami-Dade | Cooper Crane',
  desc='Crane and boom truck service for rooftop AC units across Palm Beach, Broward and Miami-Dade. Condensers and air handlers set clean on the curb. Call (954) 445-6186.',
  kw='ac unit crane lift, rooftop hvac crane, condenser lift broward, air handler crane miami',
  img='cc-rooftop-lift.jpg',
  alt='Cooper Crane boom truck setting a rooftop AC unit at sunset in Southeast Florida',
  cap='Boom truck making a rooftop set on the Atlantic coast.',
  lede='HVAC crews call us more than anyone else. Condensers, air handlers and full package units set straight onto the curb, on single-family roofs and on high-rise decks.',
  intro='<p>An AC change-out lives or dies on the lift. The unit has to come off the truck, clear the roofline, and land square on a curb that is often the same footprint as the crate. <strong>We do this several times a week across Broward and Miami-Dade</strong>, so the part your crew is worried about is the part we do every day.</p><p>Most residential change-outs are a 17-ton boom truck and under two hours on site. Commercial package units, tight courtyards, and anything past the second floor is where the 35-ton and 40-ton machines earn their keep.</p>',
  h2a='What we need before we roll',
  pts=[('Unit weight','Off the spec sheet or the crate label. Most residential condensers run 150 to 400 lb; commercial packages go well past a ton.'),
       ('Roof height and setback','How high the deck is and how far in from the curb line the unit has to travel.'),
       ('Where the truck can sit','Driveway, street, alley. Overhead power lines are the single biggest thing that changes the plan.'),
       ('Curb ready or not','If the curb or pad is not finished we can still set it aside, but you will pay for a second trip.')],
  h2b='How it usually runs',
  outro='<p>We show up, set outriggers, and your crew rigs while we spec the pick. Old unit comes off, new unit goes on, we pull the boom in and clear the site. Most single change-outs are done inside a two-hour window, which is why we can usually fit an emergency into the same week.</p><p>If a tenant is without cooling, say so when you call. We will tell you honestly whether we can get there today or whether you are better off calling someone else.</p>',
  spec=[('Typical machine','17-ton boom truck'),('Common weight range','150 lb to 2+ tons'),('Usual time on site','1 to 2 hours'),('Operator','Certified, included')]),

 dict(slug='pest-control-tarp-lifts', pre='Pest-control tarps', nav='Tarp Lifts',
  name='Pest-Control Tarp Lifts',
  h1='Fumigation Tarp Lifts for Pest-Control Crews',
  title='Fumigation Tarp Crane Lifts, South Florida | Cooper Crane',
  desc='Crane support for fumigation tenting across Palm Beach, Broward and Miami-Dade. Tarps lifted over the roofline so your crew tents faster and safer. Call (954) 445-6186.',
  kw='fumigation tarp crane, tenting crane south florida, pest control crane lift broward',
  img='work-residential.jpg',
  alt='Cooper Crane boom truck working over a Southeast Florida residential roofline',
  cap='Working over a residential roofline in Broward County.',
  lede='Tenting a two-story house by hand is slow, and it is where crews get hurt. We fly the tarps over the ridge so your team stays on the ground and the tent goes up in a fraction of the time.',
  intro='<p>Fumigation companies were some of Cooper Crane\'s first steady customers, and it is still one of the lifts we are called for most. <strong>The crane does the dangerous part</strong>: getting heavy, wind-catching tarps up and over a roofline without dragging them across tile or shingle.</p><p>We work to your schedule, not ours. Most tent jobs are early-morning starts so the structure is sealed before the day heats up, and we plan the pick around your seal-and-clamp crew.</p>',
  h2a='What makes a tarp job go smoothly',
  pts=[('Roof pitch and height','Steep tile roofs need a higher pick point so nothing drags. Tell us the storey count and roof type.'),
       ('Wind','The reason tarp lifts get rescheduled. We will call it honestly rather than fight a gusty morning.'),
       ('Truck access','Driveways are usually fine. Tight cul-de-sacs and narrow easements may push us to the spider crane.'),
       ('Your crew size','We lift, you seal. The faster your ground crew clamps, the shorter the bill.')],
  h2b='Repeat work, standing rates',
  outro='<p>If you tent regularly we would rather set up a standing arrangement than quote you one house at a time. Several South Florida pest-control companies have run with us for years on that basis, and it means your jobs get slotted first when the schedule tightens.</p><p>Call the yard with your typical volume and we will talk through what that looks like.</p>',
  spec=[('Typical machine','17-ton boom truck'),('Best for','1 to 3 storey structures'),('Scheduling','Early-morning starts'),('Repeat volume','Standing arrangements available')]),

 dict(slug='truss-setting', pre='Trusses or roofing material', nav='Trusses',
  name='Roof &amp; Floor Truss Setting',
  h1='Roof and Floor Truss Setting for Framing Crews',
  title='Roof &amp; Floor Truss Crane Setting, South Florida | Cooper Crane',
  desc='Truss setting by crane across Palm Beach, Broward and Miami-Dade. Roof and floor packages flown to your framing crew on schedule. Call (954) 445-6186.',
  kw='truss setting crane, roof truss crane south florida, framing crane broward, floor truss lift miami',
  img='work-boom-yard.jpg',
  alt='Cooper Crane Peterbilt boom truck staged with the boom extended for a truss set',
  cap='Boom truck staged and ready for a truss package.',
  lede='Your framing crew is only as fast as the truss on the hook. We keep the packages moving so the crew stays on the wall plate instead of standing around waiting.',
  intro='<p>Truss setting is a rhythm job. The crane is not the expensive part of the day; <strong>an idle framing crew is</strong>. That is why we would rather talk through the sequence before we arrive than figure it out on site with six guys on the clock.</p><p>Send the truss layout ahead if you have it. Knowing the longest span and the heaviest single truss lets us bring one machine that can reach the far gable instead of two that cannot.</p>',
  h2a='Plan the set before the truck rolls',
  pts=[('Longest span and heaviest truss','These two numbers pick the machine. Everything else is detail.'),
       ('Where the bundles are stacked','If the delivery dropped them on the far side of the lot, that is extra picks and extra hours.'),
       ('Crane position','We need a spot that reaches both gable ends without repositioning if we can get one.'),
       ('Crew readiness','Wall plates ready, bracing on hand. We can set fast, but only as fast as the crew ties off.')],
  h2b='Girder trusses and the awkward ones',
  outro='<p>Multi-ply girder trusses, long-span commercial packages and anything that has to fly over an existing structure are where we bring the 35-ton or the 40-ton out. Those are also the picks where an experienced operator matters most, and every Cooper Crane machine comes with one.</p><p>If you are bidding a job and need a crane number to price it, call before you submit. We will give you a real figure, not a placeholder.</p>',
  spec=[('Typical machine','17 to 40 ton, span dependent'),('Best sent ahead','Truss layout / span sheet'),('Usual time on site','Half day to full day'),('Operator','Certified, included')]),

 dict(slug='roofing-material-lifts', pre='Trusses or roofing material', nav='Roofing',
  name='Roofing Material Lifts',
  h1='Roofing Material Lifts, Tile and Shingle',
  title='Roofing Material Crane Lifts, Broward &amp; Miami-Dade | Cooper Crane',
  desc='Tile and shingle bundles hoisted to the deck by crane across Palm Beach, Broward and Miami-Dade. Faster loading, less roof damage. Call (954) 445-6186.',
  kw='roofing crane lift, tile loading crane south florida, shingle lift broward, roof loading miami',
  img='cc-boom-truck.jpg',
  alt='A branded Cooper Crane Peterbilt boom truck working a Southeast Florida job site',
  cap='Cooper Crane iron on a Southeast Florida job site.',
  lede='Carrying tile up a ladder is the slowest and most expensive way to load a roof. We put the whole pallet on the deck in one pick, where your crew wants it.',
  intro='<p>South Florida runs on tile, and tile is heavy. A single pallet of concrete tile can run north of 3,000 lb, which is a full morning of ladder work for a crew that should be laying underlayment instead.</p><p><strong>One crane, one morning, and the roof is loaded.</strong> We spot pallets where the crew is working rather than dumping everything at one corner, which keeps the load spread across the structure and keeps your guys from dragging tile across a finished field.</p>',
  h2a='Getting the load placement right',
  pts=[('Tile or shingle, and how much','Pallet count and material type. Concrete, clay and metal all load differently.'),
       ('Where each stack goes','Spreading the load matters structurally and saves your crew hours of walking.'),
       ('Roof condition','If we are loading over a finished or fragile field, tell us before we swing.'),
       ('Delivery timing','Best case, the material truck and the crane are on site in the same window.')],
  h2b='Tear-off and debris',
  outro='<p>The lift works in both directions. If you are tearing off, we can bring the old material down in bins instead of down a chute, which is faster on a tight lot and a lot cleaner on a finished driveway.</p><p>Tell us on the call whether you want the crane for load-up, tear-off, or both, and we will price the whole window rather than nickel and diming each pick.</p>',
  spec=[('Typical machine','17-ton boom truck'),('Common pallet weight','2,000 to 3,500 lb'),('Usual time on site','2 to 4 hours'),('Also handles','Tear-off debris bins')]),

 dict(slug='generator-lifts', pre='Generator', nav='Generators',
  name='Generator Lifts',
  h1='Standby Generator Lifts and Placement',
  title='Generator Crane Lifts, Palm Beach to Miami-Dade | Cooper Crane',
  desc='Standby and industrial generator lifts by crane across Palm Beach, Broward and Miami-Dade. Set onto pads, roofs and platforms. Call (954) 445-6186.',
  kw='generator crane lift, standby generator placement south florida, industrial generator crane broward',
  img='work-generator.jpg',
  alt='Cooper Crane boom truck setting a large industrial generator in Southeast Florida',
  cap='Setting an industrial generator in Southeast Florida.',
  lede='Generators are dense, awkward and expensive. They also tend to live in the worst possible spot: a side yard behind a fence, or a roof deck four storeys up.',
  intro='<p>Hurricane season keeps this one busy. Residential standby units, commercial sets and rooftop installs all come down to the same problem: <strong>a very heavy object that has to land exactly on the anchor bolts</strong>, often over a wall, a pool cage or a finished driveway.</p><p>We set them slow and we set them square. An operator who rushes a generator pick is how pads get cracked and how enclosures get scratched before the thing has ever run.</p>',
  h2a='What we ask about first',
  pts=[('Dry weight of the set','Off the nameplate or the spec sheet. Residential standby is often 400 to 800 lb; commercial sets run several tons.'),
       ('Pad or roof, and how far in','Reach is usually the constraint, not capacity. A light unit far from the truck needs a bigger machine than a heavy one up close.'),
       ('What we have to clear','Pool cages, walls, fences, awnings and power lines all change the pick.'),
       ('Anchor set ready','If the pad is poured and the bolts are set, we can land it once and be done.')],
  h2b='Rooftop and platform sets',
  outro='<p>Rooftop generator work is the 35-ton and 40-ton end of our fleet, and it is the kind of lift where the crane has to reach high and far at the same time. Send a photo of the building and the intended location and we will tell you straight whether it is a one-crane job.</p><p>For emergency replacement after a storm, call the yard directly. Schedules move fast in that window and the phone gets you a real answer quicker than a form.</p>',
  spec=[('Typical machine','17 to 40 ton, reach dependent'),('Residential standby','Often 400 to 800 lb'),('Send if you can','Photo of the site and pad'),('Storm season','Call, do not email')]),

 dict(slug='spider-crane-tight-access', pre='Something else', nav='Spider Crane',
  name='Spider Crane &amp; Tight Access',
  h1='Mini Spider Crane for Tight and Indoor Access',
  title='Mini Spider Crane Rental, Indoor &amp; Tight Access | Cooper Crane',
  desc='2-ton mini spider crane for indoor and tight-access lifts across Palm Beach, Broward and Miami-Dade. Fits through a 36-inch gate. Call (954) 445-6186.',
  kw='mini spider crane rental, indoor crane south florida, tight access crane miami, glass installation crane broward',
  img='cc-spider-indoor.jpg',
  alt='Cooper Crane mini spider crane working an indoor glass installation inside a Florida atrium',
  cap='Spider crane on an indoor glass install at MiamiCentral.',
  lede='When the job is inside a building, behind a gate, or in a courtyard a boom truck will never reach, the 2-ton spider crane goes where the big iron cannot.',
  intro='<p>The spider fits through a standard 36-inch gate, tracks across finished floors on rubber pads, and sets its own outriggers once it gets where it is going. <strong>We have run it inside atriums, through side yards and across plaza decks</strong>, including indoor glass work at MiamiCentral.</p><p>It is the machine that turns a "that cannot be craned" job into a normal Tuesday. Glass panels, HVAC in a mechanical room, statuary, equipment swaps in a basement plant room, hot tubs into a screened patio.</p>',
  h2a='Where the spider earns its money',
  pts=[('Indoor and atrium work','Glass, fixtures and equipment inside a finished building without tearing out a wall.'),
       ('Gated side yards','If a person can walk it, the spider can usually track it.'),
       ('Finished surfaces','Rubber tracks and spread pads instead of a 30,000 lb truck on your pavers.'),
       ('Elevated decks and plazas','Where load ratings rule out anything bigger.')],
  h2b='And everything else on the odd list',
  outro='<p>Trees, structural steel, signage, hot tubs, safes, statuary, aquariums, equipment swaps. If you can rig it, we can usually lift it, and if we genuinely cannot we will tell you that on the phone instead of billing you for a look.</p><p>Send a photo of the access route with your call. Nine times out of ten that single picture answers every question we would otherwise have to ask.</p>',
  spec=[('Machine','2-ton mini spider crane'),('Minimum gate width','36 inches'),('Surfaces','Rubber tracks, spread pads'),('Also on both','Boom trucks up to 40 ton')]),
]

def nav_block():
    return """<nav class="site-nav" id="siteNav">
  <div class="nav-inner">
    <a href="../../" class="nav-logo" aria-label="Cooper Crane home">
      <span class="mk star" aria-hidden="true">&#9733;</span>
      <span><span class="wm">Cooper Crane</span><span class="tag">Southeast Florida Crane Service</span></span>
    </a>
    <ul class="nav-links">
      <li><a href="../../#fleet">The Fleet</a></li>
      <li><a href="../../#lift">What We Lift</a></li>
      <li><a href="../../#how">How It Works</a></li>
      <li><a href="../../#area">Service Area</a></li>
      <li><a href="../../#faq">FAQ</a></li>
    </ul>
    <div class="nav-right">
      <a href="tel:%s" class="nav-phone" data-call>%s</a>
      <a href="../../#contact" class="btn btn-sm">Get a Lift Quote</a>
    </div>
    <div class="mobile-actions">
      <a href="tel:%s" class="mobile-call" aria-label="Call Cooper Crane" data-call>
        <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.6 21 3 13.4 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.2.2 2.4.6 3.6.1.3 0 .7-.2 1l-2.3 2.2z"/></svg>
      </a>
      <button class="hamburger" id="hamburger" aria-label="Open menu" aria-controls="navDrawer" aria-expanded="false"><span></span><span></span><span></span></button>
    </div>
  </div>
</nav>

<div class="nav-overlay" id="navOverlay"></div>
<aside class="nav-drawer" id="navDrawer" aria-hidden="true">
  <div class="drawer-header">
    <span class="wm"><span class="star" aria-hidden="true">&#9733;</span>Cooper Crane</span>
    <button class="drawer-close" id="drawerClose" aria-label="Close menu">&times;</button>
  </div>
  <nav class="drawer-links" aria-label="Mobile navigation">
    <a href="../../">Home</a>
    <a href="../../#fleet">The Fleet</a>
    <a href="../../#lift">What We Lift</a>
    <a href="../../#how">How It Works</a>
    <a href="../../#work">Recent Lifts</a>
    <a href="../../#area">Service Area</a>
    <a href="../../#faq">FAQ</a>
  </nav>
  <div class="drawer-footer">
    <a href="tel:%s" class="drawer-phone" data-call>
      <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.6 21 3 13.4 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.2.2 2.4.6 3.6.1.3 0 .7-.2 1l-2.3 2.2z"/></svg>
      %s
    </a>
    <a href="../../#contact" class="btn drawer-cta">Get a Lift Quote</a>
  </div>
</aside>""" % (PHONE_H, PHONE_D, PHONE_H, PHONE_H, PHONE_D)

def footer_block(cur_slug):
    others = ''.join(
        '\n        <li><a href="../%s/">%s</a></li>' % (s['slug'], s['nav'])
        for s in SERVICES if s['slug'] != cur_slug)
    return """<footer>
  <div class="footer-inner">
    <div class="footer-brand">
      <span class="wm"><span class="star" aria-hidden="true">&#9733;</span>Cooper Crane</span>
      <p class="tag">Southeast Florida Crane Service</p>
      <p>Certified-operator crane and boom truck service across Palm Beach, Broward and Miami-Dade, from a 2-ton mini spider crane to a 40-ton mobile crane.</p>
      <address>
        <a href="tel:%s" class="big" data-call>%s</a>
        <a href="mailto:Coopercranefl@gmail.com">Coopercranefl@gmail.com</a>
        <span>West Park, FL. Serving the Atlantic coast, West Palm Beach to South Miami.</span>
      </address>
      <div class="footer-social"><a href="https://www.facebook.com/CooperCraneFL" target="_blank" rel="noopener">Facebook</a></div>
    </div>
    <div class="footer-col">
      <h4>Explore</h4>
      <ul>
        <li><a href="../../">Home</a></li>
        <li><a href="../../#fleet">The Fleet</a></li>
        <li><a href="../../#how">How Booking Works</a></li>
        <li><a href="../../#why">Why Cooper</a></li>
        <li><a href="../../#work">Recent Lifts</a></li>
        <li><a href="../../#faq">FAQ</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <h4>Service Area</h4>
      <ul>
        <li><a href="../../#area">Palm Beach County</a></li>
        <li><a href="../../#area">Broward County</a></li>
        <li><a href="../../#area">Miami-Dade County</a></li>
        <li><a href="../../#area">West Palm Beach</a></li>
        <li><a href="../../#area">Fort Lauderdale</a></li>
        <li><a href="../../#area">Miami</a></li>
      </ul>
    </div>
    <div class="footer-col wide">
      <h4>Other Lifts</h4>
      <ul>%s
      </ul>
    </div>
  </div>
  <div class="footer-bottom">
    <span>&copy; 2026 Cooper Crane LLC. All rights reserved.</span>
    <a class="built-by" href="https://crossdesigned.com" target="_blank" rel="noopener" aria-label="Website built by Cross Designs">
      <span>Built by</span>
      <img src="../../assets/cross-designs.png" alt="Cross Designs">
    </a>
  </div>
</footer>""" % (PHONE_H, PHONE_D, others)

JS = """<script>
if ('scrollRestoration' in history) { history.scrollRestoration = 'auto'; }
(function () {
  function track(n, p) { if (typeof window.gtag === 'function') { window.gtag('event', n, p || {}); } }
  document.querySelectorAll('a[data-call]').forEach(a => a.addEventListener('click', () => track('call_click', { location: 'service-page' })));
  const hamburger = document.getElementById('hamburger');
  const drawer = document.getElementById('navDrawer');
  const overlay = document.getElementById('navOverlay');
  const drawerClose = document.getElementById('drawerClose');
  function openDrawer() { drawer.classList.add('open'); overlay.classList.add('open'); document.body.classList.add('drawer-open'); drawer.setAttribute('aria-hidden','false'); hamburger.setAttribute('aria-expanded','true'); }
  function closeDrawer() { drawer.classList.remove('open'); overlay.classList.remove('open'); document.body.classList.remove('drawer-open'); drawer.setAttribute('aria-hidden','true'); hamburger.setAttribute('aria-expanded','false'); }
  hamburger.addEventListener('click', openDrawer);
  drawerClose.addEventListener('click', closeDrawer);
  overlay.addEventListener('click', closeDrawer);
  drawer.querySelectorAll('a').forEach(a => a.addEventListener('click', closeDrawer));
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && drawer.classList.contains('open')) closeDrawer(); });
  (function () {
    const form = document.getElementById('qq');
    if (!form) return;
    const steps = [...form.querySelectorAll('.qq-step')];
    const bars = [...form.querySelectorAll('.qq-bars i')];
    const count = document.getElementById('qqCount');
    const sel = document.getElementById('qqSel');
    const selVal = document.getElementById('qqSelVal');
    const done = document.getElementById('qqDone');
    let cur = 0;
    function picked() { const r = form.querySelector('input[name=load]:checked'); return r ? r.value : ''; }
    function paintSel() { const v = picked(); if (v && cur > 0) { selVal.textContent = v; sel.classList.add('on'); } else sel.classList.remove('on'); }
    function show(i) {
      cur = i;
      steps.forEach((s, n) => s.classList.toggle('on', n === i));
      bars.forEach((b, n) => b.classList.toggle('on', n <= i));
      if (count) count.textContent = 'Step ' + (i + 1) + ' / 3';
      form.querySelectorAll('.qq-err').forEach(e => e.classList.remove('show'));
      paintSel();
    }
    function valid(i) {
      const err = document.getElementById('qqE' + (i + 1));
      let ok = true;
      if (i === 0) ok = !!picked();
      if (i === 1) ok = form.where.value.trim().length > 1;
      if (i === 2) ok = form.name.value.trim().length > 0 && form.phone.value.trim().length > 0;
      if (!ok && err) err.classList.add('show');
      return ok;
    }
    form.querySelectorAll('input[name=load]').forEach(r => r.addEventListener('change', () => {
      document.getElementById('qqE1').classList.remove('show');
      if (cur === 0) setTimeout(() => show(1), 140); else paintSel();
    }));
    document.getElementById('qqChange').addEventListener('click', () => show(0));
    form.querySelectorAll('.qq-next').forEach(b => b.addEventListener('click', () => { if (valid(cur)) show(Math.min(cur + 1, steps.length - 1)); }));
    form.querySelectorAll('.qq-back').forEach(b => b.addEventListener('click', () => show(Math.max(cur - 1, 0))));
    form.querySelectorAll('input').forEach(el => el.addEventListener('input', () => { const e = document.getElementById('qqE' + (cur + 1)); if (e) e.classList.remove('show'); }));
    form.addEventListener('submit', e => {
      e.preventDefault();
      if (form.company.value) return;
      if (!valid(2)) return;
      track('qualify_lead', { form_name: 'lift-ticket' });
      const subject = encodeURIComponent('Lift quote request: ' + form.name.value.trim());
      const body = encodeURIComponent('What needs lifting: ' + (picked() || '(not given)') +
        '\\nWhere: ' + form.where.value.trim() +
        '\\nHeight / weight: ' + (form.reach.value.trim() || '(not given)') +
        '\\n\\nName/business: ' + form.name.value.trim() +
        '\\nPhone: ' + form.phone.value.trim() +
        '\\nEmail: ' + (form.email.value.trim() || '(not given)'));
      window.location.href = 'mailto:Coopercranefl@gmail.com?subject=' + subject + '&body=' + body;
      steps.forEach(s => s.classList.remove('on'));
      sel.classList.remove('on');
      done.classList.add('on');
      if (count) count.textContent = 'Done';
      bars.forEach(b => b.classList.add('on'));
    });
    const pre = form.getAttribute('data-preselect');
    if (pre) { const hit = [...form.querySelectorAll('input[name=load]')].find(r => r.value === pre); if (hit) { hit.checked = true; show(1); } }
  })();

  document.querySelectorAll('.acc-header').forEach(btn => {
    btn.addEventListener('click', () => {
      const item = btn.parentElement;
      const isOpen = item.classList.contains('open');
      document.querySelectorAll('.acc-item').forEach(i => { i.classList.remove('open'); const b = i.querySelector('.acc-header'); if (b) b.setAttribute('aria-expanded','false'); });
      if (!isOpen) { item.classList.add('open'); btn.setAttribute('aria-expanded','true'); }
    });
  });
})();
</script>"""

def build(s):
    url = BASE + 'services/' + s['slug'] + '/'
    faqs = [
      ('Do you provide the crane operator?', 'Yes. Every Cooper Crane machine comes with a certified, experienced operator who handles the rigging and signaling. There is no separate operator to hire.'),
      ('Which areas do you cover for %s?' % s['name'].replace('&amp;','and').lower(), 'Every job from West Palm Beach to South Miami: Palm Beach, Broward and Miami-Dade counties, out of one Broward yard on one number, (954) 445-6186.'),
      ('How do I know what size crane I need?', 'Tell us how heavy the load is, how high it has to go and how far the crane has to reach, plus any access limits. We spec the right machine on the call, and we pick the smallest one that safely does the job.'),
      ('How far ahead should I book?', 'Earlier is better for scheduling, but we keep multiple machines in the yard and will always try to work in urgent and same-week lifts.'),
    ]
    faq_html = ''.join(
      '\n        <div class="acc-item"><button class="acc-header" aria-expanded="false">%s <span class="pm" aria-hidden="true">+</span></button><div class="acc-content"><div class="acc-text">%s</div></div></div>' % (q, a)
      for q, a in faqs)
    faq_ld = json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
      {"@type":"Question","name":q.replace('&amp;','&'),"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]}, indent=2)
    svc_ld = json.dumps({"@context":"https://schema.org","@type":"Service",
      "name":s['name'].replace('&amp;','&'),"serviceType":s['name'].replace('&amp;','&'),
      "description":s['desc'].replace('&amp;','&'),"url":url,
      "provider":{"@type":"LocalBusiness","name":"Cooper Crane LLC","@id":BASE+"#business",
        "telephone":"+1-954-445-6186","email":"Coopercranefl@gmail.com",
        "address":{"@type":"PostalAddress","addressLocality":"West Park","addressRegion":"FL","postalCode":"33023","addressCountry":"US"}},
      "areaServed":[{"@type":"AdministrativeArea","name":n} for n in ["Palm Beach County, FL","Broward County, FL","Miami-Dade County, FL"]],
      "availableChannel":{"@type":"ServiceChannel","servicePhone":{"@type":"ContactPoint","telephone":"+1-954-445-6186"},"serviceUrl":url}}, indent=2)
    crumb_ld = json.dumps({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
      {"@type":"ListItem","position":1,"name":"Home","item":BASE},
      {"@type":"ListItem","position":2,"name":"What We Lift","item":BASE+"#lift"},
      {"@type":"ListItem","position":3,"name":s['name'].replace('&amp;','&'),"item":url}]}, indent=2)

    pts = ''.join('\n        <li><span class="mk" aria-hidden="true">&#9632;</span><div><b>%s.</b> %s</div></li>' % (a, b) for a, b in s['pts'])
    spec = ''.join('\n          <div class="row"><dt>%s</dt><dd>%s</dd></div>' % (a, b) for a, b in s['spec'])
    others = ''.join(
      '\n      <a class="other-card" href="../%s/"><b>%s</b><span>View &rarr;</span></a>' % (o['slug'], o['nav'])
      for o in SERVICES if o['slug'] != s['slug'])

    return """<!DOCTYPE html>
<!-- Cooper Crane LLC | %(name)s -->
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
<meta name="twitter:image:alt" content="Cooper Crane LLC. Crane and boom truck service, West Palm Beach to South Miami. (954) 445-6186.">

<link rel="icon" type="image/png" href="../../assets/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Big+Shoulders:opsz,wght@10..72,600..800&family=Public+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">

<script type="application/ld+json">
%(svc_ld)s
</script>
<script type="application/ld+json">
%(crumb_ld)s
</script>
<script type="application/ld+json">
%(faq_ld)s
</script>

%(style)s
%(extra)s
</head>
<body>

%(nav)s

<header class="sp-hero">
  <div class="sp-hero-bg" style="background-image:url('../../assets/%(img)s')" aria-hidden="true"></div>
  <div class="sp-hero-inner">
    <nav class="crumbs" aria-label="Breadcrumb">
      <a href="../../">Home</a><span>&rsaquo;</span><a href="../../#lift">What We Lift</a><span>&rsaquo;</span>%(name)s
    </nav>
    <h1>%(h1)s</h1>
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
      <figure class="sp-photo">
        <img src="../../assets/%(img)s" alt="%(alt)s" loading="lazy">
        <figcaption>%(cap)s</figcaption>
      </figure>
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
      <div class="sp-spec">
        <b>Quick spec</b>
        <dl>%(spec)s
        </dl>
      </div>
    </aside>
  </div>
</section>

<section class="sp-quote">
  <div class="sp-quote-inner">
    <div class="sp-quote-copy">
      <div class="rule" aria-hidden="true"></div>
      <h2 class="headline">Price This Lift</h2>
      <p>Already on the right page, so we have filled in the first question. <strong>Change it if your job is something else</strong> and send it either way.</p>
      <p>Three questions, then we call you back with a real number.</p>
      <span class="alt-call">Rather talk it out? <a href="tel:%(ph)s" data-call>%(phd)s</a></span>
    </div>
%(qq)s
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
    <div class="accordion">%(faq_html)s
    </div>
  </div>
</section>

<section class="sp-other alt">
  <div class="fleet-head" style="max-width:1100px;margin:0 auto 26px;">
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
""" % dict(name=s['name'], title=s['title'], desc=s['desc'], kw=s['kw'], url=url, base=BASE,
           svc_ld=svc_ld, crumb_ld=crumb_ld, faq_ld=faq_ld, style=STYLE, extra=EXTRA_CSS,
           nav=nav_block(), img=s['img'], h1=s['h1'], lede=s['lede'], ph=PHONE_H, phd=PHONE_D,
           intro=s['intro'], alt=s['alt'], cap=s['cap'], h2a=s['h2a'], pts=pts, h2b=s['h2b'],
           outro=s['outro'], spec=spec, faq_html=faq_html, others=others,
           footer=footer_block(s['slug']), js=JS, qq=qq_form(s['pre']))

for s in SERVICES:
    d = os.path.join('services', s['slug'])
    os.makedirs(d, exist_ok=True)
    out = build(s)
    assert '—' not in out, 'em dash in ' + s['slug']
    open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(out)
    print('wrote', d, len(out), 'bytes')

# sitemap
urls = [BASE] + [BASE + 'services/' + s['slug'] + '/' for s in SERVICES]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for u in urls:
    pr = '1.0' if u == BASE else '0.8'
    sm += '  <url><loc>%s</loc><lastmod>2026-08-10</lastmod><priority>%s</priority></url>\n' % (u, pr)
sm += '</urlset>\n'
open('sitemap.xml', 'w', encoding='utf-8').write(sm)
print('sitemap:', len(urls), 'urls')
