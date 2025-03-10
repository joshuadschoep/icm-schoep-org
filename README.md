# ICM Calculator

This simple webapp is a serverless calculator for ICM, useful for poker or other tournaments where payouts are based on survivorship.

## Tech Stack

This is meant to be used via AWS and is therefore built using AWS CloudFormation templates. The code, however, is agnostic and can be run on anything as long as new infrastructure is provisioned.

The `/infra/` directory contains CloudFormation templates for serverless API config (Api.yaml), Lambda defs (Backend.yaml), and app info (App.yaml). I intend to add in a documentDB stack that will log entries and errors for monitoring.

The `/api/` directory contains relevant code and testing software for 2 python Serverless methods to calculate ICM. All lambda relevant code has been separated into some helper files for request/response as well as `*_handler.py` modules. The two methods, Malmuth-Harville and Tysen, are two well-recognized methods for calculating these probabilities. The current build is in Python 3, however I will plan time to release other versions of the API in NodeJS and Golang. These won't act differently, but I want to practice my backend lanaguages.

The `/app/` directory contains an Astro/React application that can call the relevant backend service and display useful data about the result. Astro was chosen for its quick and easy SSG for non-client code, and React was chosen as an almost industry standard for JS applications and form management. Let some love be sharaed with other [FE Frameworks](https://gist.github.com/tkrotoff/b1caa4c3a185629299ec234d2314e190), however React is what I know and what is common these days.

tl;dr:
The from-user-to-metal stack is:

- Astro SSG serving up
- A React form, connected to
- A set of python calculators
- Running on AWS Lambda

## Local Development

Separating the calculators in the backend allows you to run each of them either as a REPL, or to import them into other relevant test methods. I have some _very_ bare-bones and experimental test code included under `/api/test/`, but more can easily be added.

If contributers want to connect with the FE locally, a quick Flask or Django handler could be set up fairly quickly. I found that creating a quick dev version of my functions worked fast enough to not need to program this, however.

On that note, scripts have been included that do the same basic actions that a CD pipeline would do to deploy. Using your environment, you can very quickly spin up dev versions of the API and Lambdas.

The app itself is an Astro app, and can be run using `npm run dev` after a quick `npm install`. Check out the Astro and React docs for more information on this.

## Philosophies

ICM has essentially become a standard for how to split a rank-paid tournament without having to finish it.
Every "player" in an ICM calculation plays a perfect game where their odds of winning are proportional to their stack.

For some discussions, there is the caveat that player skill cannot be accounted for.
In my opinion, any calculation attempting to account for player skill would be somewhat arbitrary and could be disputed more easily.

### Algorithms

This calculator provides access to two algorithms for calculating ICM: The original
[Malmuth-Harville](https://www.jstor.org/stable/2284068) equation, and the
[Tysen Method](https://forumserver.twoplustwo.com/15/poker-theory-amp-gto/new-algorithm-calculate-icm-large-tournaments-1098489/), coined on twoplustwo forums.

The Malmuth-Harville equation is a multi-step Bayes probability calculation.
It works by calculating each player's odds of placing in each position, and gives them that proportion of that payout. The sum of these is their ICM calculated payout. This algorithm is pure, however it does have to run on all permutations of the players, which gives it factorial time complexity.

The Tysen method is a Monte Carlo simulation of the same, with linear complexity that can solve the problem for larger groups. Each game is simulated in a similar way to the Malmuth-Harville equation -- each player has a chance of winnig proportional to their stack. With enough iterations, we can generate an identical structure as the Malmuth-Harville equation in linear time.

The error is inversely-proportional to the square root of the iteration count. We run the simulation 100,000 times when using this algorithm.

### Data Reporting

Since ICM has become a tool for performing game-theory-optimal actions, past chopping remaining pots once the adults get tired, I wanted to give a better set of data representations than seen on similar calculators.
Graphs comparing each player's take compared to eachothers, their take relative to the original payouts, and other important data.

Other requested data models would happily be considered.
