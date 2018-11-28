public class Data {
    private double theta;
    private double distance;
    private int quality;

    public Data (double theta, double distance, int quality) {
        this.theta = theta;
        this.distance = distance;
        this.quality = quality;
    }

    public double getTheta(){
        return this.theta;
    }

    public double getDistance(){
        return this.distance;
    }

    public int getQuality(){
        return this.quality;
    }

}
