Frame Activated Unified STory Understanding System

A single unified structure to deal with events, plot units, affect

FAUSTUS represents each class of knowledge structure as a frame

## Pamela?

Norvig used to call this program Pamela, but changed it into FAUSTUS (cf: Into the heart of the mind - Frank Rose,  1984)

## Components

FAUSTUS is composed of three main components,

* one for linguistic processing
* one for frame-based inferences
* one for storyunderstanding specific inferences

Input is processed by PHRAN (Wilensky) which creates CD structures

## Data structures

Everything is a frame. There are different kinds of frames:

* Object frame
* Plan and goal frame
* Story point frame

## Process

Everything is a frame. The system instantiates frames. There's an active frame buffer. The frame has defaults and they are overriden while reading: a process called elaboration.

Frame selection:

"The problem is how to find the supermarket-shopping frame, even though it was never explicitly mentioned. The solution implemented in FAUSTUS relies on spreading activation and hierarchical composition. The basic rule is that all parts of all frames can potentially be used to find a frame (that is, we are not restricted to a small set of “triggers” for each frame), but in practice the following system is used: (1) if the input matches one unique frame, then (2) If a few frames are instantiate that frame. matched, consider each one and try to make a choice among them. (3) If the input matches a large number of frames, spread “activation energy” to each frame, and check to see if the total energy exceeds a predefined threshold necessary for instantiation.

## Papers

Frame activated inferences in a story understanding program - Norvig (1983)
Six Problems for Story Understanders - Norvig (1983)
KODIAK - a knowledge representation language - Wilensky (1984)
A Unified Theory of Inference for Text Understanding (PhD thesis) - Norvig (1987)
