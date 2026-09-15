package com.example.myapplication.model;

public class Subject {
    private int id;
    private String subjectName;
    private String subjectCode;

    public Subject() {}

    public Subject(int id, String subjectName, String subjectCode) {
        this.id = id;
        this.subjectName = subjectName;
        this.subjectCode = subjectCode;
    }

    public Subject(String subjectName, String subjectCode) {
        this.subjectName = subjectName;
        this.subjectCode = subjectCode;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
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

    @Override
    public String toString() {
        return subjectName + " (" + subjectCode + ")";
    }
}
