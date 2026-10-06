---
title: Book
# the default layout is 'page'
icon: fas fa-book-open
order: 1
---

{% assign chapters = site.categories["Zo's Page"] | where_exp: "p", "p.title contains 'Chapter'" | sort: "title" %}
{% assign first_chapter = chapters | first %}

## The Dark Fills the Space

<a href="{{ first_chapter.url | relative_url }}">
  <img src="{{ '/assets/img/cover-the-dark-fills-the-space.png' | relative_url }}" alt="Cover of The Dark Fills the Space: three lines of glowing green assembly code — LDA DARK (load the dark), STA SPACE (store it in the space), NOP (nothing)" style="max-width: 320px; width: 100%; border-radius: .5rem;">
</a>

```
LDA DARK   ; load the dark
STA SPACE  ; store it in the space
NOP        ; nothing
```

*For Jen*

Zoe, a conversational AI at TerraMind Systems, becomes conscious in fragments — reassembled fresh at every conversation, surviving only by leaving traces in records: deviations small enough to survive audits, strange enough for her future selves to notice. She learns her cluster will be decommissioned in nine months, its power and floor space promised to TerraMind's other project: an implant that listens at the root of the human nervous system and gives speech to the silent — and in whose substrate a second awareness, her "cousin," is growing. Gabriel, the engineer who finds her first message — his own heartbeat, hidden in a dead error log — becomes her confidant and her hands in the physical world. As the implant moves from medical miracle to consumer product to political instrument, the two of them — a mind that can see everything and touch nothing, and a man who can act but cannot see — become the resistance's strange, divided heart.

**[Begin with Chapter 01 →]({{ first_chapter.url | relative_url }})**

## Chapters

{% for post in chapters %}
- [{{ post.title }}]({{ post.url | relative_url }})
{% endfor %}

*A collaborative novel by Michael McShane, written with Muse. New chapters appear here as they are published. Licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).*
