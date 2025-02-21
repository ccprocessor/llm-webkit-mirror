
public class VirtualizedRadioButtonBehavior : Behavior<RadioButton>
{
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
        BindingExpression binding = AssociatedObject.GetBindingExpression(RadioButton.IsCheckedProperty);
        if (null != binding)
        {
            binding.UpdateSource();
        }
    }
}

