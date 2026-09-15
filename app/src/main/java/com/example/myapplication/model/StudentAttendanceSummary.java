package com.example.myapplication.model;

public class StudentAttendanceSummary {
    private String subjectName;
    private String subjectCode;
    private int totalClasses;
    private int attendedClasses;
    private double percentage;

    public StudentAttendanceSummary() {}

    public StudentAttendanceSummary(String subjectName, String subjectCode, int totalClasses, int attendedClasses, double percentage) {
        this.subjectName = subjectName;
        this.subjectCode = subjectCode;
        this.totalClasses = totalClasses;
        this.attendedClasses = attendedClasses;
        this.percentage = percentage;
    }

    public String getSubjectName() {
        return subjectName;
    }

    public void setSubjectName(String subjectName) {
        this.subjectName = subjectName;
    }

    public String getSubjectCode() {
        return subjectCode;
    }

    public void setSubjectCode(String subjectCode) {
        this.subjectCode = subjectCode;
    }

    public int getTotalClasses() {
        return totalClasses;
    }

    public void setTotalClasses(int totalClasses) {
        this.totalClasses = totalClasses;
    }

    public int getAttendedClasses() {
        return attendedClasses;
    }

    public void setAttendedClasses(int attendedClasses) {
        this.attendedClasses = attendedClasses;
    }

    public double getPercentage() {
        return percentage;
    }

    public void setPercentage(double percentage) {
        this.percentage = percentage;
    }
}
