import android.app.Activity;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.Bundle;
import android.widget.ImageView;

public class SensorActivity extends Activity implements SensorEventListener {
 private SensorManager mSensorManager;
 private Sensor mSensor;
 ImageView iv;

 @Override
 protected void onCreate(Bundle savedInstanceState) {
  // TODO Auto-generated method stub
  super.onCreate(savedInstanceState);
  setContentView(R.layout.sensor_screen);
  mSensorManager = (SensorManager) getSystemService(SENSOR_SERVICE);
  mSensor = mSensorManager.getDefaultSensor(Sensor.TYPE_PROXIMITY);
  iv = (ImageView) findViewById(R.id.imageView1);
 }

 protected void onResume() {
  super.onResume();
  mSensorManager.registerListener(this, mSensor,
    SensorManager.SENSOR_DELAY_NORMAL);
 }

 protected void onPause() {
  super.onPause();
  mSensorManager.unregisterListener(this);
 }

 public void onAccuracyChanged(Sensor sensor, int accuracy) {
 }

 public void onSensorChanged(SensorEvent event) {
  if (event.values[0] == 0) {
   iv.setImageResource(R.drawable.near);
  } else {
   iv.setImageResource(R.drawable.far);
  }
 }
}