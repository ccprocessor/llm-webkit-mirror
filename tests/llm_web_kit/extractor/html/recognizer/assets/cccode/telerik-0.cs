
public const string RowDataPropertyName = "RowData";
private ObservableCollection<DetailsGridRowModel> m_RowData;
public ObservableCollection<DetailsGridRowModel> RowData
{
    get
    {
        return m_RowData;
    }
    set
    {
        if (m_RowData == value)
        {
            return;
        }

        m_RowData = value;
        OnNotifyPropertyChanged(RowDataPropertyName);
    }
}

