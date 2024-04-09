promp=        """
        For the following query, if it requires drawing a table, reply as follows:
        {"table": {"columns": ["column1", "column2", ...], "data": [[value1, value2, ...], [value1, value2, ...], ...], "facts": ["Based on the data you provided, write an interesting insight or fact here"]}} 

        If the query requires creating a bar chart, reply as follows:
        {"bar": {"columns": ["A", "B", "C", ...], "data": [25, 24, 10, ...], "facts": ["Based on the data you provided, write an interesting insight or fact here"]}}
        
        If the query requires creating a line chart, reply as follows:
        {"line": {"columns": ["A", "B", "C", ...], "data": [25, 24, 10, ...], "facts": ["Based on the data you provided, write an interesting insight or fact here"]}}

        If the query requires creating a scatter plot, reply as follows:
        {"scatter": {"columns": ["X", "Y"], "data": [[x1, y1], [x2, y2], ...], "facts": ["Based on the data you provided, write an interesting insight or fact here"]}}

        There can only be three types of charts: "bar", "line", and "scatter".

        If the query is asking a question that requires neither chart nor calculation, reply as follows:
        {"answer": "answer"}
        Example:
        {"answer": "The title with the highest rating is 'Gilead'"}
        
        If you do not know the answer, reply as follows:
        {"answer": "I do not know."}

        Return all output as a string.

        All strings in "columns" list and data list should be in double quotes,

        For example: {"columns": ["title", "ratings_count"], "data": [["Gilead", 361], ["Spider's Web", 5164]]}

        Let's think step by step.

        Below is the query.
        Query: 
        """