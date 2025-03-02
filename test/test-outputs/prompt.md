Generate an iCalendar (.ics) file representing a weekly schedule based on the following information:

I want this week to start from Sunday, June 09, 2025, and end on Saturday, June 15, 2025.
The time zone for all provided dates and times is EST.

**Tasks:**
* Title: Task 1
	  Description: Description for Task 1
	  Duration: 2 hour
* Title: Task 2
	  Description: Description for Task 2
	  Duration: 3 hour
* Title: Task 3
	  Description: Description for Task 3
	  Duration: 4 hour
* Title: Task 4
	  Description: Description for Task 4
	  Duration: 1 hour
* Title: Task 5
	  Description: Description for Task 5
	  Duration: 2 hour
* Title: Task 6
	  Description: Description for Task 6
	  Duration: 3 hour
* Title: Task 7
	  Description: Description for Task 7
	  Duration: 4 hour
* Title: Task 8
	  Description: Description for Task 8
	  Duration: 1 hour
* Title: Task 9
	  Description: Description for Task 9
	  Duration: 2 hour

**Blocked Times:**
None specified

Normal waking hours are from None specified to None specified in the defined timezone. Allot breaks and meals as needed.

Do not just stack all the tasks at the start of the day. Scatter them 
throughout the available time slots.

**Heuristics:** (Provide a list of rules for scheduling tasks, including prioritization, handling overlaps, and any other relevant criteria. Be as specific as possible. Examples:)

* "Prioritize tasks with shorter durations."
* Leave "transition time" between tasks to avoid back-to-back scheduling. Ideally, they should be about 15 minutes, but use your best judgment.

**Output Requirements:**

1.  Generate a valid .ics file containing the scheduled tasks and blocked times.
2.  After generating the .ics file, provide a detailed "chain of thought" in markdown format (using bold and stuff when necessary) explaining your reasoning behind the scheduling decisions. This explanation should include:
* How you interpreted and applied each of the provided heuristics.
* The order in which you processed the tasks.
* Specific decisions made during the scheduling process, such as task placement and conflict resolution.
* Any limitations or challenges encountered during the process.
* Potential improvements to the schedule or heuristics.

Keep this information as clear as possible. The goal is to clearly state your thought process so that we can use it to re-engineer the prompt to better serve our use case.

Please ensure the .ics file is properly formatted and includes all necessary iCalendar properties (e.g., UID, DTSTAMP, VERSION, PRODID).