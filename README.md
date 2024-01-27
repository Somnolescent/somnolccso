# SomnolCCSO
This is our WIP homespun script for the CCSO/Ph server we use on gopher.somnolescent.net. dcb originally wrote it around May 29, 2019 and got it functional July 6, 2020. Circa mid-January 2024, we've given it a repo so we can continue work on it together.

SomnolCCSO is functional, but currently a little rough around the edges. It's read-only by design--while CCSO does have editing and authentication functionality, none of that is implemented in our script. This is meant to be a simple, easy-to-deploy Python CCSO server for the curious. All database updates are done "offline" by editing the entries.json file in the same folder as the script. A sample entries.json file with some of our own entries is included in this repo.

## Features
- Commands: status, fields, query
- Reads database entries from JSON

## Dependencies
Python 3.7.
