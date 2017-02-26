# Microsoft-Azure

On Azure :
Created a web service that allows a user to login, and upload either: a textual note or a single picture (these may be a
grocery list, a reminder, a todo list, a picture of a bag of rice, or similar – a quick note or picture).
Each note or picture have a one-word subject (such as “todo” or “groceries”), these subject words do not need
to be unique (there may be several grocery lists), and each note or picture have a priority (10 is very important,
0 is not important). Each picture or note have an upload time associated with it.
A user is able to upload a note or picture, set the subject, and priority; or, see notes and pictures
(for that user), sorted by time and date (youngest or oldest first), or priority, or subject.
Users will be able to delete a note or picture.
Multiple users may use your service simultaneously.
restricted picture sizes, note sizes, and limit number of pictures and notes, per user.

Scaling a web service
On Azure:
web service automatically scale to support more, simultaneous, use.
Multiple users will be able to post and inspect pictures and notes concurrently, and the system should not
slow down, your goal should be 1 second (2 second maximum) response.
Suggestion: Use jmeter (or similar) to stress test and validate your system.
