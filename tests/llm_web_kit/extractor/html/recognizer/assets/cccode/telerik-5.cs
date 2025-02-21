
using System.Collections.Generic;
using System.Windows.Controls;
using System.ComponentModel;

namespace GridViewCellTemplateBug
{
    public partial class MainPage : UserControl
    {
        public MainPage()
        {
            InitializeComponent();
            ProductCollection itemList = new ProductCollection();
            for (int i = 0; i < 100; i++)
            {
                Product item = new Product();
                item.Selected = true;
                item.SKUDescription = "Description" + i.ToString() + "   number" + i.ToString() + i.ToString();
                itemList.Add(item);
            }
            rgvProducts.ItemsSource = itemList;
        }
    }

    public class Product : object, INotifyPropertyChanged
    {
        private bool _Selected;
        public string SKUDescription { get; set; }
        public bool Selected
        {
            get { return _Selected; }
            set
            {
                _Selected = value;
                NotifyPropertyChanged("Selected");
            }
        }
        public event PropertyChangedEventHandler PropertyChanged;
        public void NotifyPropertyChanged(string propertyName)
        {
            if (PropertyChanged != null)
            {
                PropertyChanged(this, new PropertyChangedEventArgs(propertyName));
            }
        }
    }
    public class ProductCollection : List<Product>
    {
        public ProductCollection() : base() { }
        public ProductCollection(Product[] items)
            : base()
        {
            if (items != null)
            {
                foreach (Product item in items)
                {
                    this.Add(item);
                }
            }
        }
    };
}

