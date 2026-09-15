package com.example.myapplication.model;

public class AttendanceRecord {
    private int id;
    private String studentRoll;
    private String studentName;
    private int subjectId;
    private String date;
    private String status; // "PRESENT" or "ABSENT"

    public AttendanceRecord() {}

    public AttendanceRecord(int id, String studentRoll, String studentName, int subjectId, String date, String status) {
        this.id = id;
        this.studentRoll = studentRoll;
        this.studentName = studentName;
        this.subjectId = subjectId;
        this.date = date;
        this.status = status;
    }

    public AttendanceRecord(String studentRoll, String studentName, int subjectId, String date, String status) {
        this.studentRoll = studentRoll;
        this.studentName = studentName;
        this.subjectId = subjectId;
        this.date = date;
        this.status = status;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getStudentRoll() {
        return studentRoll;
    }

    public void setStudentRoll(String studentRoll) {
        this.studentRoll = studentRoll;
    }

    public String getStudentName() {
        return studentName;
    }

    public void setStudentName(String studentName) {
        this.studentName = studentName;
    }

    public int getSubjectId() {
        return subjectId;
    }

    public void setSubjectId(int subjectId) {
        this.subjectId = subjectId;
    }

    public String getDate() {
        return date;
    }

    public void setDate(String date) {
        this.date = date;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }
}
