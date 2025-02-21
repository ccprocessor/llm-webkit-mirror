
public class VirtualizedRadioButtonBehavior : Behavior<RadioButton>
    {
        public DependencyProperty SynchronizedPropertyProperty = DependencyProperty.Register("SynchronizedProperty", typeof(bool?), typeof(VirtualizedRadioButtonBehavior), new PropertyMetadata(null));

        public bool? SynchronizedProperty
        {
            get { return (bool?)GetValue(SynchronizedPropertyProperty); }
            set { SetValue(SynchronizedPropertyProperty, value); }
        }

        protected override void OnAttached()
        {
            AssociatedObject.LayoutUpdated += AssociatedObject_LayoutUpdated;
            base.OnAttached();
        }

        protected override void OnDetaching()
        {
            AssociatedObject.LayoutUpdated -= AssociatedObject_LayoutUpdated;
            base.OnDetaching();
        }

        void AssociatedObject_LayoutUpdated(object sender, EventArgs e)
        {
            if (SynchronizedProperty != AssociatedObject.IsChecked)
            {
                AssociatedObject.IsChecked = SynchronizedProperty;
            }
        }
    }

