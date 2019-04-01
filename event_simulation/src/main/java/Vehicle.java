package main.java;

public class Vehicle {
    int id;
    float len;
    float width;
    int type; // vehicle class
    float startTime;
    float endTime;
    float velocity;


    int section;


    public Vehicle(int id, float len, float width, int type, float velocity, int section, float startTime, float endTime) {
        this.id = id;
        this.len = len;
        this.width = width;
        this.type = type;
        this.velocity = velocity;
        this.section = section;
        this.startTime = startTime;
        this.endTime = endTime;
    }
    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public float getLen() {
        return len;
    }

    public void setLen(float len) {
        this.len = len;
    }

    public float getWidth() {
        return width;
    }

    public void setWidth(float width) {
        this.width = width;
    }

    public int getType() {
        return type;
    }

    public void setType(int type) {
        this.type = type;
    }

    public float getStartTime() {
        return startTime;
    }

    public void setStartTime(float startTime) {
        this.startTime = startTime;
    }

    public float getEndTime() {
        return endTime;
    }

    public void setEndTime(long endTime) {
        this.endTime = endTime;
    }
    public int getSection() {
        return section;
    }

    public void setSection(int section) {
        this.section = section;
    }


}
