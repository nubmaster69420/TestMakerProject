# TestMakerProject
 A simple program which gets a file(CSV/Excel) with tasks and creates different variants
You only have to upload a file(Using a a toolbar or a shortcut ctr+O), choose a number of variants, and check a radio button if you want to create a variant for retake(The fron design was created in QTDesigner). After, when you press a button "Create", the program starts making variants using a special algorithm that was made by myself(Based on "itertools" and "random" modules). The algorithm returns a dict of variants and warnings(if they appear), or it may return an exitcode in case of error.
After this the main program displays variants in a table, and the user can save it in a word file using buttons "save"(ctr+S) and "save as"(shift+ctrl+S) in the toolbar.
