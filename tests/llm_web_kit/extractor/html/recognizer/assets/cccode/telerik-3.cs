
public class BasicStructureToImageConverter  :IValueConverter
    {

        public object Convert(object value, Type targetType, object parameter, System.Globalization.CultureInfo culture)
        {
            string imageName = value as string;
            Uri uri = new Uri(@"http://localhost:6449" + "/images/"
                       + HttpUtility.UrlEncode(imageName) + ".png", UriKind.Absolute);
            return new BitmapImage(uri);
        }

        public object ConvertBack(object value, Type targetType, object parameter, System.Globalization.CultureInfo culture)
        {
            throw new NotImplementedException();
        }
    }

