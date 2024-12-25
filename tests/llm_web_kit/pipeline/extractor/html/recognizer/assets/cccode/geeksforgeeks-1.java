public class MyStuff
{
    String name;

    MyStuff(String n) {  name = n;  }

    public static void main(String[] args)
    {
        MyStuff m1 = new MyStuff("guitar");
        MyStuff m2 = new MyStuff("tv");
        System.out.println(m2.equals(m1));
    }

    @Override
    public boolean equals(Object obj)
    {
        MyStuff m = (MyStuff) obj;
        if (m.name != null)  { return true;  }
        return false;
    }
}