====== {{event.start|date:"F"}} {{event.start.year}} SLUG Meeting ======

====Summary====

 * Date: Friday, {{event.start}}
 * Start: Arrive at 6pm for a 6:30pm start
 * Format: TBA
 * RSVP: http://{{ request.get_host }}{{event.get_url}}
 * Suggest or sign up for a talk at http://{{ request.get_host }}/talks

==== Details ====

{% for item in agenda %}
  - {{ item.offer.displayname }} - {{ item.offer.title }}
{% empty %}
Details TBA.
{% endfor %}

====Location====

  Google Sydney
  Level 5, Workplace 6
  48 Pirrama Road
  Pyrmont, NSW

 Map: http://{{ request.get_host }}/map

-- Getting there --

The Google office is the big black building marked "Accenture" opposite
Star City Pirrama Road facade.

If using the trains, you can go either get off at;

 * Town Hall station, head towards Darling Harbour, walk across the Pyrmont
   footbridge and then follow Pirrama Road towards Star city.
 * Central station, then follow the light rail instructions.

If using the buses, the route 443 stops right out front of the building.

If using the light rail, get off at Star City station and walk across the
street.

If you drive, then you can look for parking on the suburban streets around
the office (or pay for parking at the Casino), and then walk from there.

=== Afterwards ===

We'll be aiming to finish by 8pm and will be heading to the Pyrmont Bridge
Hotel (PBH) afterwards to socalise and eat dinner. The PBH is marked on the
map.
