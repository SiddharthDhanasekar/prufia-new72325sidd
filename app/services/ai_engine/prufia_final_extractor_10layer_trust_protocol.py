# PRUFIA FULL 10-LAYER EXTRACTOR FRAME WITH TRUST BOOST LOGIC
import re
from typing import Dict
from difflib import SequenceMatcher

class PrufiaExtractor10Layer:
    def __init__(self):
        self.traits = {
            'biographical_consistency': [
                # Blue collar/working class (1-25)
                "my dad worked double shifts at the plant", "mama cleaned houses to pay rent", "we lived paycheck to paycheck",
                "I started bagging groceries at fourteen", "my uncle taught me to weld in the garage", "grandpa fixed cars in the backyard",
                "we shopped at thrift stores every weekend", "I walked to school in worn-out shoes", "our trailer park had one payphone",
                "my first job was washing dishes at Denny's", "dad came home covered in grease and dirt", "we ate beans and rice most nights",
                "I dropped out sophomore year to work", "got my GED at the community center", "worked construction since I was sixteen",
                "mama did hair in our kitchen for extra money", "we hunted deer for dinner on weekends", "I learned to fix everything myself",
                "our town had more churches than grocery stores", "I milked cows every morning before school", "we grew vegetables in the backyard",
                "my hands been dirty since I was little", "never owned nothing brand new growing up", "we made do with hand-me-downs always",
                "I been working since I could reach the counter", "my back's been bad from heavy lifting for years",
                
                # Professional/educated/college (26-50)
                "during my residency at Johns Hopkins Medical Center", "I defended my doctoral dissertation on quantum mechanics", "my undergraduate thesis focused on behavioral economics",
                "as a senior partner at the law firm", "I published extensively in peer-reviewed academic journals", "my MBA program at Wharton emphasized strategic leadership",
                "in medical school we studied advanced pathophysiology", "my fellowship research involved cardiovascular interventions", "as department chair I oversee curriculum development",
                "my doctorate in psychology took seven rigorous years", "I'm licensed to practice in multiple states", "board certification requires continuous professional development",
                "my private practice specializes in pediatric cardiology", "I lecture graduate students at the university", "peer review committees evaluate research proposals",
                "continuing education mandates keep us current", "my residency was particularly grueling at Mass General", "academic tenure demands original research contributions",
                "research grants from NIH fund my laboratory", "I mentor doctoral candidates in their dissertations", "conference presentations showcase cutting-edge findings",
                "my clinical experience spans two decades of practice", "evidence-based protocols guide all treatment decisions", "interdisciplinary collaboration improves patient outcomes",
                "professional development workshops enhance clinical skills", "my expertise in corporate mergers and acquisitions",
                
                # High school/teenage (51-65)
                "in freshman year I was awkward and weird", "my homecoming date totally stood me up", "I failed algebra twice and had to retake",
                "detention was basically my second home unfortunately", "I played JV basketball but rode the bench", "prom was honestly overrated and expensive",
                "I got suspended for skipping too many classes", "my crush didn't even know I existed sadly", "I absolutely hated PE class with passion",
                "lunch table politics were brutal and dramatic", "I lived for Friday night football games", "my locker was always messy and disorganized",
                "I got grounded literally every other week", "yearbook signing made me emotional and nostalgic", "I couldn't wait to finally graduate and leave",
                
                # Elementary/childhood (66-75)
                "in third grade I accidentally wet my pants", "my teacher Mrs. Johnson was really mean", "I brought lunch in crumpled brown bags",
                "recess was absolutely the best part ever", "I collected Pokemon cards obsessively", "show and tell made me super nervous",
                "I rode the yellow school bus every morning", "my mom packed peanut butter and jelly sandwiches", "I was terrified of the dark basement",
                "I lost my first tooth eating a green apple",
                
                # Seniors/elderly (76-85)
                "back in my day we walked everywhere", "I remember when gas cost thirty cents", "we didn't have all these electronic gadgets",
                "my arthritis acts up whenever it rains", "I've buried way too many good friends", "retirement ain't what I expected it to be",
                "my grandkids teach me about computers and phones", "social security barely covers my monthly rent", "I take six different pills every morning",
                "my doctor appointments fill up the entire calendar",
                
                # Rural/farming (86-95)
                "we planted crops by the moon phases", "harvest season meant absolutely no sleep for weeks", "I can tell tomorrow's weather by tonight's sky",
                "our well went completely dry last summer", "I've delivered baby calves at two in the morning", "the bank threatened foreclosure on the farm",
                "we sold fresh eggs at the Saturday farmer's market", "my hands are permanently stained from working soil", "I know every single inch of this land",
                "four AM sharp means feeding time for animals",
                
                # Medical professionals (96-100)
                "my patient presented with acute respiratory symptoms", "I completed my residency in emergency medicine", "medical school at Harvard was incredibly demanding", "I specialize in pediatric cardiac surgery", "my practice focuses on geriatric psychiatry"
            ],
            
            'metacognitive_awareness': [
                # Simple/uneducated reflection (1-20)
                "I didn't know no better back then", "it took me forever to figure that out", "I was just plain stupid about it",
                "somebody shoulda told me different", "I wish I knew then what I know now", "I been doing it wrong this whole time",
                "took me years to finally catch on", "I finally got some sense knocked into me", "I used to be real hardheaded about everything",
                "mama tried to warn me but I wouldn't listen", "I had to learn the lesson the hard way", "looking back now I see it clear",
                "I was too proud to ask for help", "now I understand what they meant", "I shoulda listened to my elders",
                "it finally clicked for me one day", "I been thinking about it all wrong", "somebody finally set me straight eventually",
                "I had my head up in the clouds", "reality hit me like a freight train",
                
                # Professional/educated reflection (21-40)
                "upon further reflection I realize my error", "my initial hypothesis was fundamentally flawed", "subsequent analysis revealed significant gaps",
                "I've reconsidered my theoretical position", "empirical evidence suggests otherwise conclusively", "my cognitive biases clearly influenced judgment",
                "metacognitive strategies improved my understanding substantially", "I engaged in rigorous critical self-reflection", "paradigm shifts required considerable mental flexibility",
                "I questioned my foundational assumptions systematically", "intellectual humility demanded serious reconsideration", "epistemological frameworks evolved through study",
                "I subjected beliefs to rigorous scientific scrutiny", "philosophical inquiry led to profound insights", "dialectical thinking revealed inherent contradictions",
                "I embraced cognitive dissonance constructively", "systematic introspection yielded remarkable clarity", "I recognized confirmation bias patterns",
                "phenomenological analysis deepened self-awareness significantly", "I interrogated my research methodology thoroughly",
                
                # Teenage reflection (41-55)
                "I thought I knew everything in high school", "I was so cringe and embarrassing back then", "I can't believe I used to think that",
                "looking back I was pretty immature honestly", "I thought I was so cool but wasn't", "my teenage brain was absolutely wild",
                "I wish I could tell my younger self", "I was trying way too hard to fit in", "I thought all adults were completely stupid",
                "I made some really dumb choices back then", "peer pressure got to me really bad", "I was going through a weird phase",
                "I thought that love would last forever", "high school drama seemed so important then", "I was way too emotional about everything",
                
                # Working class reflection (56-70)
                "I didn't think much about it back then", "work taught me things school never did", "I learned just by watching other people",
                "trial and error was my only teacher", "common sense finally kicked in eventually", "I figured it out completely on my own",
                "real experience taught me way better", "I learned to think before I acted", "mistakes cost me money I couldn't afford",
                "I had to swallow my pride eventually", "other workers showed me the ropes", "I learned to keep my mouth shut",
                "I realized I wasn't as smart as I thought", "hard work beat book learning any day", "I learned to listen way more",
                
                # Medical reflection (71-85)
                "my diagnostic reasoning was clearly incomplete", "I failed to consider important differential diagnoses", "clinical judgment required significant refinement",
                "I should have ordered additional diagnostic tests", "my bedside manner definitely needed improvement", "I overlooked several subtle symptoms",
                "continuing education revealed serious knowledge gaps", "peer consultation challenged my thinking patterns", "evidence-based practice evolved my approach",
                "I recognized my knowledge limitations clearly", "clinical experience taught professional humility", "I learned from poor patient outcomes",
                "medical errors prompted serious reflection", "I needed to update protocols immediately", "patient feedback was truly illuminating",
                
                # Academic reflection (86-100)
                "my theoretical framework was insufficient", "I needed to challenge basic assumptions", "interdisciplinary perspectives enriched understanding significantly",
                "I recognized disciplinary blind spots clearly", "peer review exposed serious weaknesses", "I needed broader methodological training",
                "my literature review was inadequate", "I failed to consider alternative interpretations", "my research design had major limitations",
                "I needed to interrogate data more rigorously", "collaborative work revealed hidden biases", "I should have triangulated findings",
                "my conclusions exceeded available evidence", "I needed stronger theoretical grounding", "I overlooked contradictory studies completely"
            ],
            
            'emotion_gradient': [
                # Basic/working class emotional expression (1-25)
                "I was mad as hell about it", "that really ticked me off bad", "I was fit to be tied completely",
                "it made my blood boil hot", "I was happy as a clam", "scared the bejesus right out of me",
                "I was madder than a wet hen", "that just broke my heart completely", "I was pleased as punch",
                "nervous as a long-tailed cat in a room full of rocking chairs", "I was dumber than dirt",
                "angrier than a hornet", "I felt lower than dirt", "I was tickled pink",
                "scared completely out of my wits", "I was beside myself with worry", "that really got my goat",
                "I was walking on air", "I felt like death warmed over", "I was sick as a dog",
                "that really burned me up inside", "I was grinning from ear to ear", "I felt like I'd been hit by a truck",
                "my heart was pounding out of my chest", "I was shaking like a leaf",
                
                # Professional emotional expression (26-45)
                "I experienced significant cognitive dissonance", "the emotional impact was professionally profound", "I felt intellectually validated",
                "there was considerable psychological distress", "I experienced impostor syndrome acutely", "the stress manifested somatically",
                "I felt professionally stimulated", "there was substantial emotional labor involved", "I experienced severe compassion fatigue",
                "the ethical dilemma created significant anxiety", "I felt professionally conflicted", "there was notable moral distress present",
                "I experienced decision fatigue", "the workload created burnout symptoms", "I felt professionally isolated",
                "there was significant role ambiguity", "I experienced performance anxiety", "the responsibility felt overwhelming",
                "I felt professionally compromised", "there was emotional exhaustion present",
                
                # Teenage emotional expression (46-60)
                "I literally wanted to die of embarrassment", "I was so embarrassed I could literally die", "I was shaking I was so mad",
                "my heart was like beating out of my chest", "I felt so awkward and weird", "I was crying so hard I couldn't breathe",
                "I was literally shaking with pure anger", "I felt like such a complete loser", "I was so excited I literally couldn't even",
                "I wanted to crawl in a hole and die", "I was so nervous I thought I'd throw up", "I felt like everyone was staring at me",
                "I was so happy I was literally crying", "I felt so stupid and ugly", "I was so scared I completely froze up",
                
                # Medical emotional expression (61-75)
                "the patient's condition deteriorated rapidly", "I felt the weight of clinical responsibility", "there was palpable family distress",
                "I experienced vicarious trauma", "the prognosis created emotional burden", "I felt professionally inadequate",
                "there was significant moral distress", "I experienced decision-making anxiety", "the outcome was emotionally devastating",
                "I felt the gravity of life-and-death decisions", "there was profound grief in the room", "I experienced compassion satisfaction",
                "the family's pain was absolutely heartbreaking", "I felt the privilege of healing", "there was beautiful resilience displayed",
                
                # Academic emotional expression (76-90)
                "I experienced intellectual exhilaration", "there was a profound eureka moment", "I felt academically validated",
                "the research created existential anxiety", "I experienced impostor syndrome deeply", "there was intellectual intimidation",
                "I felt cognitively overwhelmed", "the discovery was intellectually thrilling", "I experienced academic insecurity",
                "there was philosophical disorientation", "I felt intellectually inadequate", "the complexity was cognitively taxing",
                "I experienced theoretical confusion", "there was methodological anxiety", "I felt academically isolated",
                
                # Senior emotional expression (91-100)
                "my heart's not what it used to be", "I get emotional much easier these days", "that brings back bittersweet memories",
                "I feel the weight of all these years", "my emotions are closer to the surface", "I cry at commercials now",
                "I feel grateful for every single day", "the loneliness sometimes overwhelms me completely", "I'm more sentimental than I used to be",
                "I feel the fragility of life daily"
            ],
            
            'context_adaptation': [
                # Basic code-switching (1-20)
                "I talk different at home than at work", "I clean up my language around church folks", "I use big words when I need to impress people",
                "with my crew I keep it completely real", "at parent conferences I sound professional", "around my kids I explain things simple",
                "in job interviews I speak proper English", "with my boys I drop my guard", "at the doctor's office I ask better questions",
                "when I'm nervous I talk too fancy", "around my family I relax my speech", "in court I watch every single word",
                "at work I keep my mouth shut", "with strangers I'm more polite", "around educated people I try harder",
                "in fancy restaurants I mind my manners", "with my neighbors I can be myself", "at school events I speak carefully",
                "with customers I'm always respectful", "around my boss I choose words carefully",
                
                # Professional context switching (21-40)
                "I adjust my register for different audiences", "clinical language requires absolute precision", "interdisciplinary communication demands clarity",
                "patient education necessitates significant simplification", "academic discourse follows strict conventions", "public speaking requires accessibility",
                "technical documentation demands specificity", "cross-cultural communication requires sensitivity", "administrative meetings need diplomacy",
                "peer consultation involves professional jargon", "public presentations require audience engagement", "written reports demand formal structure",
                "client meetings need persuasive language", "team collaboration allows informal communication", "board presentations require executive language",
                "training sessions need instructional clarity", "crisis communications demand calm authority", "media interviews require sound bites",
                "grant writing follows academic conventions", "performance reviews need diplomatic language",
                
                # Educational context switching (41-55)
                "I explain differently to each grade level", "parent-teacher conferences require diplomatic tact", "faculty meetings use educational jargon",
                "student interactions need age-appropriate language", "administrative communications are strictly formal", "classroom management uses authoritative tone",
                "peer collaboration involves professional discourse", "community outreach requires accessible language", "special needs students need modified communication",
                "testing situations demand clear instructions", "disciplinary conversations require firm language", "encouraging struggling students needs warmth",
                "IEP meetings use technical terminology", "playground supervision uses simple commands", "staff development uses professional language",
                
                # Social class context switching (56-70)
                "I sound smarter when I absolutely need to", "around rich folks I watch my grammar", "with working people I keep it simple",
                "at fancy places I try to fit in", "in my neighborhood I can be myself", "with educated people I use bigger words",
                "around blue collar folks I relax completely", "at upscale events I mind my manners", "with family I drop the act",
                "in professional settings I code-switch", "around my old friends I talk normal", "at country clubs I fake it",
                "with my boss I speak carefully", "around coworkers I'm more casual", "at job interviews I sound professional",
                
                # Cultural context switching (71-85)
                "in my culture we show respect differently", "mainstream America has different rules", "my community values different things",
                "white spaces require careful code-switching", "ethnic communities understand cultural context", "assimilation demands constant adaptation",
                "cultural code-switching is daily survival", "dominant culture sets the conversational tone", "minority spaces allow authentic expression",
                "intercultural communication requires extreme sensitivity", "cultural norms vary significantly", "tradition influences expression patterns",
                "generational differences affect communication", "religious settings have specific language", "secular environments require different approach",
                
                # Age-based context switching (86-100)
                "I explain things differently to grandkids", "with young people I try to stay current", "around my age group we understand each other",
                "with teenagers I avoid sounding preachy", "elderly folks appreciate slower conversation", "children need much simpler explanations",
                "millennials communicate very differently", "baby boomers prefer direct communication", "gen z has their own language",
                "middle-aged folks get straight to business", "seniors appreciate patience and respect", "young adults want authentic interaction",
                "with kids I use animated expressions", "around elderly I speak more clearly", "teenagers need relatable examples"
            ],
            
            'domain_expertise': [
                # Blue collar expertise (1-25)
                "you gotta torque that bolt to spec", "the threads are completely stripped on this", "this weld ain't gonna hold under pressure",
                "I can hear the bearing going bad in the motor", "the hydraulics are leaking fluid again", "you need a much bigger wire gauge",
                "this concrete ain't setting right in this weather", "the grade's off by half an inch", "these studs ain't sixteen inches on center",
                "the circuit's dangerously overloaded", "this pipe's gonna burst when winter comes", "the foundation's settling wrong",
                "I've been running heavy equipment for twenty years", "you learn to listen to the engine", "I can frame a house with my eyes closed",
                "safety regulations require double fall protection", "OSHA standards are absolutely non-negotiable", "I've trained dozens of apprentices over years",
                "the tolerances on this job are tight", "this material won't meet building codes", "the inspector's gonna flag this work",
                "we need proper ventilation in here", "the load capacity's been exceeded", "this equipment needs immediate calibration",
                "the pressure's reading way too high", "these measurements are completely off",
                
                # Medical expertise (26-50)
                "the patient presents with acute respiratory symptoms", "differential diagnosis includes multiple serious conditions", "I ordered a comprehensive metabolic panel",
                "vital signs indicate possible cardiovascular compromise", "antibiotic resistance patterns strongly suggest", "surgical intervention is absolutely contraindicated",
                "post-operative complications may include serious infection", "medication interactions could potentially potentiate", "laboratory values are extremely concerning",
                "imaging reveals significant pathological changes", "prognosis depends on multiple critical factors", "evidence-based protocols strongly recommend",
                "clinical guidelines suggest alternative treatment approach", "pharmacokinetics indicate necessary dosage adjustment", "therapeutic index is dangerously narrow",
                "adverse effects include serious complications", "contraindications absolutely preclude this medication", "dosing requires careful renal adjustment",
                "the patient's condition is rapidly deteriorating", "intensive monitoring is absolutely essential", "specialist consultation is immediately indicated",
                "emergency intervention may be necessary", "the diagnosis requires confirmatory testing", "treatment response has been suboptimal",
                "side effects are becoming problematic",
                
                # Legal expertise (51-70)
                "precedent clearly establishes defendant liability", "statutory interpretation requires careful analysis", "constitutional issues are directly implicated",
                "discovery rules mandate complete disclosure", "burden of proof shifts to defendant", "summary judgment is entirely appropriate",
                "appellate review will be highly deferential", "venue is proper in this jurisdiction", "standing requirements are clearly satisfied",
                "damages calculation includes multiple factors", "settlement negotiations remain confidential", "ethical rules strictly prohibit disclosure",
                "attorney-client privilege protects all communications", "work product doctrine clearly applies", "conflict of interest analysis required",
                "professional responsibility demands immediate disclosure", "malpractice exposure is quite significant", "bar disciplinary action possible",
                "the contract terms are ambiguous", "liquidated damages clause is enforceable",
                
                # Technology expertise (71-90)
                "the algorithm complexity is exponential", "database normalization prevents data redundancy", "API endpoints require strict authentication",
                "version control manages all code changes", "unit tests verify core functionality", "deployment pipeline automates release process",
                "microservices architecture enables horizontal scalability", "load balancing distributes incoming traffic", "caching significantly improves performance",
                "security protocols encrypt all sensitive data", "user interface design affects usability metrics", "responsive design adapts to different devices",
                "debugging tools help identify issues", "code reviews ensure quality standards", "documentation facilitates ongoing maintenance",
                "backup strategies prevent catastrophic data loss", "monitoring systems track performance metrics", "disaster recovery plans ensure business continuity",
                "the system architecture is highly scalable", "performance bottlenecks need optimization",
                
                # Academic expertise (91-100)
                "the theoretical framework requires modification", "empirical evidence strongly supports hypothesis", "methodological limitations affect validity",
                "peer review process ensures quality", "statistical significance indicates correlation", "qualitative data provides rich insights",
                "literature review reveals research gaps", "interdisciplinary approach enhances understanding", "research ethics approval is mandatory",
                "data collection protocols ensure reliability"
            ],
            
            'creative_synthesis': [
                # Simple creative combinations (1-20)
                "I mixed two family recipes together", "I combined ideas from different TV shows", "I put my own personal spin on it",
                "I mashed up two songs I really liked", "I took parts from different things I saw", "I made it fit my own style",
                "I blended what I learned from both teachers", "I created something totally new and different", "I borrowed ideas and changed them around",
                "I experimented until something finally worked", "I improvised with whatever I had available", "I made it work somehow",
                "I tried different combinations until it clicked", "I mixed old and new ideas together", "I created my own version",
                "I combined what worked from each method", "I made something unique from common parts", "I blended different approaches together",
                "I took inspiration from multiple sources", "I created my own twist on tradition",
                
                # Artistic creative synthesis (21-40)
                "I synthesized multiple artistic influences", "I created hybrid art forms", "I juxtaposed contrasting visual elements",
                "I explored thematic connections across mediums", "I reimagined traditional artistic forms", "I subverted expected artistic conventions",
                "I layered symbolic meanings throughout", "I created dialogue between different genres", "I transformed source material completely",
                "I generated novel interpretations", "I fused disparate cultural traditions", "I crafted innovative expressions",
                "I challenged established artistic boundaries", "I created conceptual bridges", "I developed unique aesthetic approaches",
                "I integrated different artistic languages", "I synthesized contrasting styles", "I created unexpected combinations",
                "I merged digital and traditional techniques", "I developed original artistic vocabularies",
                
                # Academic creative synthesis (41-60)
                "I integrated multiple theoretical frameworks", "I synthesized diverse empirical findings", "I developed novel research hypotheses",
                "I created interdisciplinary connections", "I generated innovative research methodologies", "I constructed new paradigms",
                "I bridged different disciplinary boundaries", "I synthesized competing theories", "I developed original concepts",
                "I created novel analytical approaches", "I integrated diverse scholarly perspectives", "I generated creative solutions",
                "I synthesized complex literature", "I developed innovative applications", "I created theoretical extensions",
                "I merged quantitative and qualitative methods", "I synthesized contradictory findings", "I developed hybrid models",
                "I created new conceptual frameworks", "I integrated opposing viewpoints",
                
                # Professional creative synthesis (61-80)
                "I developed innovative business solutions", "I created hybrid management approaches", "I synthesized client requirements",
                "I generated novel strategic approaches", "I integrated multiple methodologies", "I created adaptive frameworks",
                "I developed creative workflows", "I synthesized stakeholder needs", "I created custom solutions",
                "I integrated diverse team perspectives", "I developed innovative processes", "I created value-added services",
                "I synthesized market research findings", "I generated creative alternatives", "I developed unique value propositions",
                "I created breakthrough strategies", "I synthesized competitive intelligence", "I developed innovative partnerships",
                "I created disruptive business models", "I synthesized customer feedback",
                
                # Technical creative synthesis (81-100)
                "I architected novel technical solutions", "I synthesized system requirements", "I created innovative algorithms",
                "I integrated multiple platforms", "I developed hybrid architectures", "I created custom frameworks",
                "I synthesized user requirements", "I generated creative workarounds", "I developed novel interfaces",
                "I integrated disparate systems", "I created innovative data models", "I synthesized performance requirements",
                "I developed creative optimization strategies", "I integrated multiple APIs", "I created novel design patterns",
                "I synthesized security requirements", "I developed innovative protocols", "I created scalable architectures",
                "I integrated legacy and modern systems", "I developed creative automation solutions"
            ],
            
            'cultural_knowledge': [
                # African American culture (1-20)
                "in our family Sunday dinner is sacred", "we don't play the dozens at church", "my mama taught me to speak up for myself",
                "that's some real talk right there", "we keep it one hundred in our house", "my grandmama didn't raise no fool",
                "church is where we get our strength", "we been through too much to give up now", "our ancestors paved the way for us",
                "we celebrate Black excellence", "our struggle is generational", "we lift as we climb always",
                "the barbershop is our safe space", "we season everything with love", "our music tells our story",
                "we dress up for church every Sunday", "respect your elders no matter what", "education is our way out",
                "we stick together through everything", "our hair is our crown",
                
                # Latino/Hispanic culture (21-40)
                "la familia comes first always", "we eat together every Sunday without fail", "mi abuela taught me everything important",
                "respeto is absolutely non-negotiable", "we celebrate with the whole community", "our traditions connect all generations",
                "we work hard for our children's future", "education is our path forward", "we honor our ancestors daily",
                "our food is made with pure amor", "we dance at every celebration", "community supports each other always",
                "we speak Spanish at home", "our culture is rich and beautiful", "we maintain our traditions proudly",
                "quinceañeras mark becoming a woman", "Day of the Dead honors family", "we gather for every holiday",
                "machismo has its place and limits", "our music connects us to home",
                
                # Asian American culture (41-55)
                "family honor is everything to us", "education is the highest priority", "we respect our elders deeply",
                "hard work is expected always", "we save face in public", "filial piety guides our actions",
                "we maintain cultural traditions", "success brings family pride", "we sacrifice for the next generation",
                "our heritage defines our identity", "we balance tradition and progress", "community reputation matters greatly",
                "we teach through example", "our ancestors guide our choices", "cultural values shape behavior",
                
                # Southern culture (56-70)
                "bless your heart means something specific", "we say ma'am and sir always", "Sunday dinner brings family together",
                "hospitality is our way of life", "we wave at everyone we pass", "sweet tea is a food group",
                "front porch conversations matter", "we know everyone's business", "church is the community center",
                "we tell stories to teach lessons", "our roots run deep here", "tradition matters more than change",
                "we help neighbors without asking", "our word is our bond", "family recipes are sacred secrets",
                
                # Rural/farming culture (71-85)
                "we work from sunup to sundown", "weather determines everything we do", "neighbors help during harvest time",
                "we fix things instead of replacing them", "livestock comes before personal comfort", "the land provides and demands respect",
                "we know every animal personally", "seasons dictate our entire schedule", "we waste absolutely nothing ever",
                "hard work builds character", "we depend on each other", "the farm is our heritage",
                "we understand life and death", "we live by nature's rhythms", "community barn raisings unite us",
                
                # Military culture (86-100)
                "mission first people always", "we leave no one behind ever", "honor courage commitment guide us",
                "chain of command is sacred", "we serve something greater", "brothers and sisters in arms",
                "duty before self always", "we adapt and overcome obstacles", "semper fi means forever faithful",
                "we earned our place here", "sacrifice is our calling", "we protect those who can't protect themselves",
                "discipline creates freedom", "we follow orders first", "we defend the Constitution daily"
            ],
            
            'revision_artifacts': [
                # Simple revision patterns (1-20)
                "wait let me say that again", "no that's not right at all", "let me fix that real quick",
                "I said that completely wrong", "hold up that's backwards", "let me try that again",
                "scratch that entirely", "never mind what I just said", "what I meant to say was",
                "let me correct myself there", "that came out all wrong", "I misspoke there badly",
                "let me back up and restart", "that's not what I meant", "I need to rephrase that",
                "let me be clearer about that", "I expressed that poorly", "let me say it better",
                "that sounded wrong", "I need to fix my words",
                
                # Academic revision patterns (21-40)
                "to clarify my previous statement", "I should amend that assertion", "let me refine that argument",
                "upon reflection I would revise", "I need to qualify that claim", "that requires further nuance",
                "I should be more precise", "let me elaborate on that point", "I want to refine my position",
                "that statement needs context", "I should clarify the parameters", "let me provide more specificity",
                "I need to modify that conclusion", "let me add important caveats", "that assertion needs qualification",
                "I should provide more evidence", "let me strengthen that argument", "that needs better support",
                "I should clarify my methodology", "let me refine my hypothesis",
                
                # Professional revision patterns (41-55)
                "let me rephrase that professionally", "I need to adjust my approach", "allow me to reconsider that",
                "I should frame that differently", "let me provide additional context", "I want to be more accurate",
                "that needs better explanation", "I should reconsider my words", "let me adjust my statement",
                "I need to be more diplomatic", "let me soften that language", "I should choose better words",
                "that requires more sensitivity", "let me be more tactful", "I should moderate my tone",
                
                # Working class revision patterns (56-70)
                "that ain't what I meant", "let me say it different", "I messed that up completely",
                "that's not how I wanted to say it", "I got my words all mixed up", "let me try that over again",
                "I said it backwards", "that's not what I was getting at", "I need to explain it better",
                "I jumbled that up", "let me straighten that out", "I got tongue-tied there",
                "I didn't say that right", "let me put it another way", "I confused myself there",
                
                # Medical revision patterns (71-85)
                "let me clarify the diagnosis", "I need to amend my assessment", "the clinical picture requires revision",
                "I should modify my treatment plan", "let me correct that medical history", "I need to update my documentation",
                "the symptoms suggest alternative diagnosis", "I should reconsider the differential", "let me revise my clinical notes",
                "I need to adjust the medication dosage", "the lab results change my assessment", "I should modify the treatment protocol",
                "let me update the patient's chart", "I need to revise my recommendations", "the imaging changes my diagnosis",
                "I should adjust my clinical approach", "let me modify the care plan", "I need to reconsider the prognosis",
                
                # Elderly revision patterns (86-100)
                "let me think about that again", "I might have that backwards", "my memory's not perfect anymore",
                "I should be more careful with my words", "let me reconsider what I said", "I might be misremembering that",
                "I need to think that through better", "I should be more thoughtful", "let me be more precise about that",
                "I might have gotten confused there", "I should double-check that information", "I need to be more careful",
                "let me correct what I just said", "I should think before I speak", "I might have mixed that up"
            ],
            
            'temporal_awareness': [
                # Basic temporal references (1-25)
                "back in my day things were different", "nowadays everything's changed completely", "when I was younger life was simpler",
                "these days kids don't understand respect", "things used to be much simpler", "in the old days we walked everywhere",
                "before cell phones even existed", "when gas was under a dollar", "back when we had real respect",
                "in my time we worked much harder", "nowadays everyone's just lazy", "when I was growing up",
                "back then we didn't have computers", "in the fifties life was better", "before the internet ruined everything",
                "when I was your exact age", "in my youth we had manners", "back when families ate together",
                "before all this modern technology", "in the good old days", "when people still talked face to face",
                "before everything got so complicated", "when neighbors actually knew each other", "back when doors stayed unlocked",
                "in simpler times people cared more",
                
                # Professional temporal awareness (26-50)
                "the paradigm has shifted significantly over time", "industry standards have evolved dramatically", "best practices have changed substantially",
                "regulatory requirements have been updated recently", "professional development has advanced considerably", "technology has transformed practice completely",
                "evidence-based approaches emerged in recent decades", "methodologies have been refined over years", "protocols have been updated regularly",
                "research has advanced our understanding significantly", "innovations have changed approaches fundamentally", "standards of care have evolved",
                "professional expectations have heightened considerably", "competency requirements have expanded dramatically", "certification standards have been upgraded",
                "continuing education mandates have increased", "technology integration has accelerated rapidly", "interdisciplinary collaboration has grown",
                "quality metrics have improved substantially", "patient expectations have risen significantly", "documentation requirements have expanded greatly",
                "liability concerns have increased over time", "ethical standards have become more stringent", "professional accountability has heightened",
                "specialization has become more narrow and focused",
                
                # Educational temporal awareness (51-70)
                "curriculum standards have changed dramatically", "teaching methods have evolved significantly", "technology has transformed education completely",
                "student needs have shifted considerably", "assessment strategies have been updated", "classroom management has adapted",
                "educational research has advanced understanding", "learning theories have developed further", "special education has expanded greatly",
                "inclusion practices have improved substantially", "parent involvement has increased", "community partnerships have grown",
                "professional development has been enhanced", "data-driven instruction has emerged", "differentiated learning has evolved",
                "cultural competency has developed", "social-emotional learning has been emphasized", "trauma-informed practices have been adopted",
                "restorative justice has been implemented", "mindfulness practices have been introduced",
                
                # Medical temporal awareness (71-90)
                "medical knowledge has advanced rapidly", "treatment protocols have evolved dramatically", "diagnostic capabilities have improved significantly",
                "pharmaceutical options have expanded greatly", "surgical techniques have been refined", "technology has revolutionized patient care",
                "evidence-based medicine has emerged", "patient safety measures have been enhanced", "quality indicators have been developed",
                "electronic records have transformed documentation", "telemedicine has expanded access", "precision medicine has advanced",
                "immunotherapy has revolutionized oncology", "minimally invasive procedures have developed", "preventive care has been emphasized",
                "population health has been focused", "healthcare delivery has been transformed", "patient engagement has increased",
                "care coordination has improved", "outcomes measurement has been enhanced",
                
                # Working class temporal awareness (91-100)
                "jobs ain't what they used to be", "benefits keep getting cut every year", "work's gotten more dangerous over time",
                "pay hasn't kept up with rising costs", "unions don't have the power anymore", "automation's been taking our jobs",
                "safety rules keep changing constantly", "training requirements have increased dramatically", "documentation has gotten more complex"
            ],
            
            'attention_fragmentation': [
                # Simple attention breaks (1-25)
                "wait what was I saying again", "I totally lost my train of thought", "where was I going with this",
                "I got distracted for a second there", "hold on let me remember", "I forgot what I was talking about",
                "my mind went completely blank", "I lost track of my point", "what was the question again",
                "sorry I completely spaced out", "I got sidetracked", "where was I at again",
                "I forgot where I was going", "my brain just stopped working", "I lost my place",
                "I was thinking about something else", "I got off track", "what were we talking about",
                "I totally blanked out", "my thoughts scattered everywhere", "I lost focus there",
                "I can't remember my point", "my mind wandered off", "I got confused",
                "sorry I'm all over the place",
                
                # Professional attention fragmentation (26-45)
                "I apologize for the mental lapse", "let me refocus on the issue", "I need to realign my thoughts",
                "I experienced momentary distraction", "let me return to the main point", "I should concentrate better",
                "my attention was divided momentarily", "I need to prioritize this discussion", "let me gather my thoughts",
                "I was processing multiple inputs", "I should focus more intently", "let me reorganize my thinking",
                "I was considering parallel issues", "my cognitive load was excessive", "I need better mental discipline",
                "I was multitasking ineffectively", "let me streamline my focus", "I should eliminate distractions",
                "my working memory was overloaded", "I need to chunk information better",
                
                # Academic attention fragmentation (46-65)
                "I was analyzing multiple variables", "my theoretical framework shifted", "I was considering alternative hypotheses",
                "the complexity overwhelmed my processing", "I was integrating diverse perspectives", "my analytical focus wavered",
                "I was weighing contradictory evidence", "the interdisciplinary connections distracted me", "I was synthesizing competing theories",
                "my critical thinking process stalled", "I was evaluating methodological issues", "the literature review overwhelmed me",
                "I was questioning my assumptions", "the epistemological implications confused me", "I was reconsidering my paradigm",
                "the philosophical foundations shifted", "I was exploring conceptual boundaries", "my intellectual curiosity scattered",
                "the research implications multiplied", "I was considering ethical dimensions",
                
                # Medical attention fragmentation (66-80)
                "I was considering differential diagnoses", "multiple symptoms required analysis", "the clinical picture was complex",
                "I was weighing treatment options", "patient history complicated assessment", "I was monitoring vital signs",
                "the lab results were concerning", "I was consulting multiple specialists", "family concerns distracted me momentarily",
                "I was documenting thoroughly", "the emergency situation demanded attention", "I was coordinating care plans",
                "the medication interactions worried me", "I was considering side effects", "the prognosis was uncertain",
                
                # Elderly attention fragmentation (81-90)
                "my mind wanders more these days", "I lose my thoughts easier now", "my concentration isn't what it was",
                "I get confused more often", "my memory skips around", "I have trouble focusing",
                "my thoughts jump between subjects", "I forget what I was saying", "my mind feels scattered",
                "my attention span has shortened",
                
                # Working class attention fragmentation (91-100)
                "my mind's on the bills", "I'm worried about work tomorrow", "got too much going on",
                "can't stop thinking about problems", "my head's all over the place", "too much stress to focus",
                "work's been on my mind", "I'm distracted by money troubles", "can't concentrate with all this pressure",
                "my thoughts keep jumping around"
            ]
        }


    def fuzzy_match(self, sentence: str, phrase: str, threshold: float = 0.6) -> bool:
        similarity = SequenceMatcher(None, sentence.lower(), phrase.lower()).ratio()
        return similarity >= threshold

    def extract(self, text: str) -> Dict:
        sentences = [s.strip() for s in re.split(r'[.!?]', text) if s.strip()]
        results = {}

        for trait, phrases in self.traits.items():
            match_count = 0
            for phrase in phrases:
                for sentence in sentences:
                    if self.fuzzy_match(sentence, phrase):
                        match_count += 1
                        break
            if phrases:
                results[trait] = round(match_count / len(phrases) * 100, 2)
            else:
                results[trait] = 0.0

        # TRUST BOOST LOGIC: If 5 or more traits score >= 60%, mark as human
        passing_traits = sum(1 for score in results.values() if score >= 60)
        results['human_verified'] = passing_traits >= 5
        return results
