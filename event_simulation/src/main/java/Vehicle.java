package main.java;

public class Vehicle {
    int id;
    double len;
    double width;
    int type; // vehicle class
    double startTime;
    double endTime;
    int enterSection;
    int exitSection;
    double velocity;


    int section;


    public Vehicle(int id, double len, double width, int type, double velocity, int section, double startTime, double endTime, int enterSection, int exitSection) {
        this.id = id;
        this.len = len;
        this.width = width;
        this.type = type;
        this.velocity = velocity;
        this.section = section;
        this.startTime = startTime;
        this.endTime = endTime;
        this.enterSection = enterSection;
        this.exitSection = exitSection;
    }
    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public double getLen() {
        return len;
    }

    public void setLen(double len) {
        this.len = len;
    }

    public double getWidth() {
        return width;
    }

    public void setWidth(double width) {
        this.width = width;
    }

    public int getType() {
        return type;
    }

    public void setType(int type) {
        this.type = type;
    }

    public double getStartTime() {
        return startTime;
    }

    public void setStartTime(double startTime) {
        this.startTime = startTime;
    }

    public double getEndTime() {
        return endTime;
    }

    public void setEndTime(double endTime) {
        this.endTime = endTime;
    }

    public int getEnterSection() {
        return enterSection;
    }

    public void setEnterSection(int enterSection) {
        this.enterSection = enterSection;
    }

    public int getExitSection() {
        return exitSection;
    }

    public void setExitSection(int exitSection) {
        this.exitSection = exitSection;
    }

    public int getSection() {
        return section;
    }

    public void setSection(int section) {
        this.section = section;
    }


}
