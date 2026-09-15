package com.example.myapplication.adapter;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.RadioButton;
import android.widget.RadioGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.example.myapplication.R;
import com.example.myapplication.model.User;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class AttendanceStudentAdapter extends RecyclerView.Adapter<AttendanceStudentAdapter.AttendanceViewHolder> {

    private final List<User> studentList;
    private final Map<String, String> attendanceMap = new HashMap<>(); // Key: Roll Number, Value: "PRESENT" or "ABSENT"

    public AttendanceStudentAdapter(List<User> studentList) {
        this.studentList = studentList;
        // Default all students to PRESENT
        for (User student : studentList) {
            attendanceMap.put(student.getUsername(), "PRESENT");
        }
    }

    public Map<String, String> getAttendanceMap() {
        return attendanceMap;
    }

    public void setAttendanceMap(Map<String, String> newMap) {
        if (newMap != null) {
            this.attendanceMap.clear();
            this.attendanceMap.putAll(newMap);
            notifyDataSetChanged();
        }
    }

    @NonNull
    @Override
    public AttendanceViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext()).inflate(R.layout.item_attendance_student, parent, false);
        return new AttendanceViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull AttendanceViewHolder holder, int position) {
        User student = studentList.get(position);
        holder.tvStudentName.setText(student.getName());
        holder.tvStudentRoll.setText("Roll No: " + student.getUsername());

        String status = attendanceMap.get(student.getUsername());
        if (status == null) status = "PRESENT";

        // Prevent recycling trigger
        holder.rgStatus.setOnCheckedChangeListener(null);

        if ("PRESENT".equalsIgnoreCase(status)) {
            holder.rbPresent.setChecked(true);
        } else {
            holder.rbAbsent.setChecked(true);
        }

        holder.rgStatus.setOnCheckedChangeListener((group, checkedId) -> {
            if (checkedId == R.id.rbPresent) {
                attendanceMap.put(student.getUsername(), "PRESENT");
            } else if (checkedId == R.id.rbAbsent) {
                attendanceMap.put(student.getUsername(), "ABSENT");
            }
        });
    }

    @Override
    public int getItemCount() {
        return studentList.size();
    }

    static class AttendanceViewHolder extends RecyclerView.ViewHolder {
        TextView tvStudentName, tvStudentRoll;
        RadioGroup rgStatus;
        RadioButton rbPresent, rbAbsent;

        public AttendanceViewHolder(@NonNull View itemView) {
            super(itemView);
            tvStudentName = itemView.findViewById(R.id.tvStudentName);
            tvStudentRoll = itemView.findViewById(R.id.tvStudentRoll);
            rgStatus = itemView.findViewById(R.id.rgStatus);
            rbPresent = itemView.findViewById(R.id.rbPresent);
            rbAbsent = itemView.findViewById(R.id.rbAbsent);
        }
    }
}
