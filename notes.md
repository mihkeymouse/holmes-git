# Notes 
#17-10
We have 3 days left, best to adapt an already existing story - my personal pick is Holmes and the adventure of Abbey Grange
The idea, is simple the game is played by a git repo 
We have school holidays at the moment and Im currently enjoying myself in Ooty


Plan is to split the plot into 5 ACTS each with a different git feature

ACT 1 - Summons
Holmes and "my dear watson" travel to abbey grange after Inspector Hopkin's telegram

ACT II - The testimonies
Lady brackenstall and theresa recount the burglary

ACT III - The crime scene 
Holmes baba examines the dining room + physical evidence

ACT IV - Contradiction arrives Holmes divergeres from the official account

ACT V - Holmes investigates eventually hitting upon the true culprit

ACT VI - verdict - The confession

#Mechanics - git log - chronology
             git show - case rec
             git diff - compare evidence
             git blame - accuse the culprit
             git branch - switch between investigative threads - difficult because m.Doyles original treatise proceeds in a linear fashion - perhaps we branch the investigation keeping plot linear

Players should experience events in watsons' OG order but  as such should be free to go back and visit

How do we prevent people from unlocking scenes prematurely? do we split across multiple git repos or is there anything simpler?

The game can use git commits as deduction gates . A  Gh action can check if its right. You fork the repo and solve the mystery
Caveat: Git hooks dont transfer with forks

#Deduction gate placements...should avoid too many gates

the Wineglasses for one
thodi thodi piya karo - pankaj udhas
The bell rope and chair // git diff comes rather naturally here
The sailors knot
The verdict

Technical design final: One player owned fork per playthrough , player pushes a deduction and a workflow judges it and an accepted answer should add Watson's next case record to the repo

We want to avoid loops due to workflow created pushes
- 
Branches for revisiting evidence. 
GH actions should be able to unlock the next scene without putting unrevealed chapters in the players local git history!

Maybe fetch each chapter from an external source?

**A push made using the workflow's GITHUB_TOKEN will not ordinarily trigger another push workflow.** That solves the loops

File structure
README
case/
    watson.md
    evidence.md
    deduction.md
.case/
    state.json
.github/
    workflows/

How do we make sure git blam workes as it is intended to accuse Capt Crocker?

git blame - responsibility aint guilt
b4 finale
case/verdict.md should contain hopkin's og accusation
holmes conclusion is undecided
watsons is undecided
the player (holmes) identifies the killer by editing case/verdict.md, commits and pushes the accusation
GH actions validates, crockers confession + trial scene unlock
The verdict - Watsons not guilty, gh sctions add watsons judgement as separate git commit and thr player runs git pull
player executes git blame case/verdict.md

So final gitblame attributes 3 conclusions to hopkins, holmes and watson