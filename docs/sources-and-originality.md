# Sources and originality

## Intellectual boundary

Blueprint Signal is independently written software. Its structure, interface, wording, checks as implemented, fictional example, documentation and visual identity were created for this repository.

It does not reproduce lecture slides, speaker notes, classroom cases, assignments, exam material, course diagrams or institution-specific teaching material. Service blueprinting as a general technique only defines the problem domain. The implementation rests on public publications.

The Fjord Table restaurant, its stages, steps, owners, durations, failure points, improvement plan and review are written in code and wholly fictional. They are not evidence about any real restaurant or customer.

## What the sources support

The same list ships inside the app (**Research & limits**), in the printable brief and in every evidence ZIP.

- **Shostack (1982)** introduced the service blueprint as a way to document a service's processes and separate what the customer sees from what happens out of sight (the line of visibility). Blueprint Signal adopts that separation.
- **Shostack (1984)** describes designing a service with a blueprint that identifies processes, isolates fail points and sets time frames. Blueprint Signal takes the idea of attaching failure points to specific steps. It records durations per step but does not set standards or sum them, because parallel work and rework make a single service time misleading.
- **Bitner, Ostrom and Morgan (2008)** set out the practical form of the blueprint used here: physical evidence, customer actions, onstage contact employee actions, backstage actions and support processes, separated by the lines of interaction, visibility and internal interaction, and its use in service innovation. Blueprint Signal follows those five layers and three lines.

No source validates the app's "questions to resolve" rules, its evidence labels, its table limits or its rework-loop warning. Those are transparent design choices.

## Primary references

- Bitner, M. J., Ostrom, A. L., & Morgan, F. N. (2008). Service blueprinting: A practical technique for service innovation. *California Management Review, 50*(3), 66–94. https://doi.org/10.2307/41166446
- Shostack, G. L. (1982). How to design a service. *European Journal of Marketing, 16*(1), 49–63. https://doi.org/10.1108/EUM0000000004799
- Shostack, G. L. (1984, January). Designing services that deliver. *Harvard Business Review*. https://hbr.org/1984/01/designing-services-that-deliver

Bibliographic details for the two journal articles were checked against Crossref. The Harvard Business Review article has no Crossref record; its title and issue month were checked against the publisher's page.

## License

Blueprint Signal is free software under AGPL-3.0-or-later. The license covers this project's expression, not ownership of published methods. The embedded interface font is distributed under the SIL Open Font License; see `src/blueprintsignal/ui/assets/fonts/OFL.txt`.
