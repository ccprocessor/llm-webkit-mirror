     .
     .
     .

int i = 0;
foreach (var col in ColumnsCollection)
{
    GridViewDataColumn column = new GridViewDataColumn();
    column.CellTemplate = GetDataboundTemplate(i);

    // do something with col here

    GridView.Columns.Add(column);
    i++;
}
     .
     .
     .

     public DataTemplate GetDataboundTemplate(int columnIndex)
        {
            StringBuilder xaml = new StringBuilder();
            xaml.Append("<DataTemplate xmlns=\" [namespace] \" xmlns:my=\" [namespace] \">");
            xaml.Append("<my:DetailsGridItemView Context=\"{Binding ColumnData[" + columnIndex + "]}\" />");
            xaml.Append("</DataTemplate>");
            DataTemplate template = XamlReader.Load(xaml.ToString()) as DataTemplate;
            return template;
        }
