[1mdiff --git a/ttkwidgets/timeline.py b/ttkwidgets/timeline.py[m
[1mindex fae8466..1f0737d 100644[m
[1m--- a/ttkwidgets/timeline.py[m
[1m+++ b/ttkwidgets/timeline.py[m
[36m@@ -245,7 +245,7 @@[m [mclass TimeLine(ttk.Frame):[m
 [m
     """[m
     Generating TimeLine contents[m
[31m-    [m
[32m+[m
     These functions all play a role in creating items in the canvases[m
     """[m
 [m
[36m@@ -286,8 +286,8 @@[m [mclass TimeLine(ttk.Frame):[m
         self._category_labels.clear()[m
         canvas_width = 0[m
         for category in (sorted(self._categories.keys() if isinstance(self._categories, dict) else self._categories)[m
[31m-                                 if not isinstance(self._categories, OrderedDict)[m
[31m-                                 else self._categories):[m
[32m+[m[32m                         if not isinstance(self._categories, OrderedDict)[m
[32m+[m[32m                         else self._categories):[m
             kwargs = self._categories[category] if isinstance(self._categories, dict) else {"text": category}[m
             kwargs["background"] = kwargs.get("background", self._background)[m
             kwargs["justify"] = kwargs.get("justify", tk.LEFT)[m
[36m@@ -564,7 +564,7 @@[m [mclass TimeLine(ttk.Frame):[m
 [m
     """[m
     Time marker functions[m
[31m-    [m
[32m+[m
     Functions to show the small time frame[m
     """[m
 [m
[36m@@ -738,7 +738,7 @@[m [mclass TimeLine(ttk.Frame):[m
 [m
     """[m
     Marker manipulation[m
[31m-    [m
[32m+[m
     These functions are bound to Tkinter events and manipulate the markers in some form or another[m
     """[m
 [m
[36m@@ -925,7 +925,7 @@[m [mclass TimeLine(ttk.Frame):[m
 [m
     """[m
     Properties[m
[31m-    [m
[32m+[m
     These properties offer up-to-date information about the state of the TimeLine[m
     """[m
 [m
