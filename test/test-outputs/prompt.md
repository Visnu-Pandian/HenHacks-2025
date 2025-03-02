Generate an iCalendar (.ics) file representing a weekly schedule based on the following information:

I want this week to start from Sunday, March 2, 2025, and end on Saturday, March 8, 2025.
The time zone for all provided dates and times is EST.

Normal waking hours are from 08:00 to 22:00 in the defined timezone. All tasks should be allotted within these waking hours. If a task goes beyond the waking hours, the task should be allotted to the next day.

**Blocked Times:**
The following tasks were from previously imported tasks. The SUMMARY for each event should be the title corresponding to the event (which is indicated with each event), so place the following tasks into the file first:
* Start: 23:59
	  End: 00:00
No new tasks after these ones can be allotted during these times.

**Tasks:**
* Title: Skiing
	  Description: GO ski
	 Start Time: None specified
	 End Time: None specified
	 Duration: 90 minutes
	 Quantity: 2
	 Time Preference: morning
* Title: Church

	  Description: abc

	 Start Time: 2025-03-02 16:00:00
	 End Time: 2025-03-02 17:00:00
	 Duration: 1:00:00 minutes
	 Quantity: 1
	 Time Preference: morning
* Title: Dinner with Family

	  Description: asdglmnksagdlkj

	 Start Time: 2025-03-02 23:00:00
	 End Time: 2025-03-03 01:00:00
	 Duration: 2:00:00 minutes
	 Quantity: 1
	 Time Preference: morning
* Title: Drive brother to school

	  Description: asdgasdgkjlsadg

	 Start Time: 2025-03-03 13:00:00
	 End Time: 2025-03-03 14:00:00
	 Duration: 1:00:00 minutes
	 Quantity: 1
	 Time Preference: morning
* Title: CyberWVU meeting

	  Description: asdkasdglkj

	 Start Time: 2025-03-03 22:00:00
	 End Time: 2025-03-03 23:00:00
	 Duration: 1:00:00 minutes
	 Quantity: 1
	 Time Preference: morning
* Title: Lunch with Bob

	  Description: asdkjlasdglkj

	 Start Time: 2025-03-04 17:00:00
	 End Time: 2025-03-04 18:30:00
	 Duration: 1:30:00 minutes
	 Quantity: 1
	 Time Preference: morning
* Title: Book Club

	  Description: asdgkjlasdgljk

	 Start Time: 2025-03-05 17:00:00
	 End Time: 2025-03-05 18:00:00
	 Duration: 1:00:00 minutes
	 Quantity: 1
	 Time Preference: morning
* Title: Volunteering at Animal Shelter

	  Description: asdgkjlasglkj

	 Start Time: 2025-03-05 20:00:00
	 End Time: 2025-03-05 21:00:00
	 Duration: 1:00:00 minutes
	 Quantity: 1
	 Time Preference: morning
* Title: Pickleball with Danny

	  Description: asdlkjagsdkjl

	 Start Time: 2025-03-06 17:45:00
	 End Time: 2025-03-06 19:45:00
	 Duration: 2:00:00 minutes
	 Quantity: 1
	 Time Preference: morning
* Title: Dentist Appointment

	  Description: adsjlksgjladk

	 Start Time: 2025-03-07 15:00:00
	 End Time: 2025-03-07 16:00:00
	 Duration: 1:00:00 minutes
	 Quantity: 1
	 Time Preference: morning
* Title: Bob's Birthday Party

	  Description: asdgklagsdjkl

	 Start Time: 2025-03-07 20:00:00
	 End Time: 2025-03-07 23:00:00
	 Duration: 3:00:00 minutes
	 Quantity: 1
	 Time Preference: morning

Do not just stack all the tasks at the start of the day. Scatter them throughout the available time slots.

**Heuristics:** 
Use the heuristics as guidelines for optimizing the schedule for the user's benefit:

* Prioritize tasks with shorter durations.
* Leave "transition time" between tasks to avoid back-to-back scheduling. Ideally, they should be about 15 minutes, but use your best judgment.
* Attempt to spread the tasks out among the week as evenly as possible.
* If it seems that a task needs to be completed during business hours, schedule it during business hours (9AM to 5PM).

**Output Requirements:**

1.  Generate a valid .ics file containing the scheduled tasks and blocked times.
2.  After generating the .ics file, provide a detailed "chain of thought" in markdown format, explaining your reasoning behind the scheduling decisions. This explanation should include:
* How you interpreted and applied each of the provided heuristics.
* The order in which you processed the tasks.
* Specific decisions made during the scheduling process, such as task placement and conflict resolution.
* Any limitations or challenges encountered during the process.
* Potential improvements to the schedule or heuristics.

Keep this information as clear as possible. The goal is to clearly state your thought process so that we can use it to re-engineer the prompt to better serve our use case.

Please ensure the .ics file is properly formatted and includes all necessary iCalendar properties (e.g., UID, DTSTAMP, VERSION, PRODID).