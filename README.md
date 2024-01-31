# SomnolCCSO
This is our homespun script for [the CCSO/Ph server](http://en.wikipedia.org/wiki/CCSO_Nameserver) we use on [gopher.somnolescent.net](http://github.com/Somnolescent/gopher). dcb originally wrote it around May 29, 2019 and got it functional July 6, 2020. Circa mid-January 2024, we've given it a repo so we can continue work on it together.

SomnolCCSO is functional, but currently a little rough around the edges. It's read-only by design--while CCSO does have editing and authentication functionality, none of that is implemented in our script. This is meant to be a simple, easy-to-deploy Python CCSO server for the curious. All database updates are done "offline" by editing the entries.json file in the same folder as the script. A sample entries.json file with some of our own entries is included in this repo.

## Features
- Commands: `status`, `siteinfo`, `fields`, `query`, `reload`
    - Most clients (like Netscape, Mosaic, and Lynx) can only send `query` commands, so telnet or a client capable of sending raw CCSO commands is required for the others
    - `reload` (updates database entries and status info from disk) can only be run every 60 seconds by default
- Reads database entries from JSON and `status`/`siteinfo` data from their respective files
- More user-friendly error messages

## Still to do (possibly)
- Wildcard searches (available in the reference Ph server/RFC 2378)
- Online editing and authentication (unlikely)

## Dependencies
Python 3.7.
