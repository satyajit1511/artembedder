package com.example.myapplication.adapter;

import android.graphics.Color;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.example.myapplication.R;
import com.example.myapplication.model.StudentAttendanceSummary;

import java.util.List;
import java.util.Locale;

public class StudentSummaryAdapter extends RecyclerView.Adapter<StudentSummaryAdapter.SummaryViewHolder> {

    private final List<StudentAttendanceSummary> summaryList;

    public StudentSummaryAdapter(List<StudentAttendanceSummary> summaryList) {
        this.summaryList = summaryList;
    }

    @NonNull
    @Override
    public SummaryViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext()).inflate(R.layout.item_student_subject_summary, parent, false);
        return new SummaryViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull SummaryViewHolder holder, int position) {
        StudentAttendanceSummary summary = summaryList.get(position);
        holder.tvSubjectName.setText(summary.getSubjectName());
        holder.tvSubjectCode.setText("Code: " + summary.getSubjectCode());
        holder.tvClassesRatio.setText(String.format(Locale.getDefault(), "Attended: %d / %d classes", summary.getAttendedClasses(), summary.getTotalClasses()));

        double percentage = summary.getPercentage();
        holder.tvPercentage.setText(String.format(Locale.getDefault(), "%.1f%%", percentage));

        if (percentage >= 75.0) {
            holder.tvPercentage.setTextColor(Color.parseColor("#2E7D32")); // Green
            holder.tvPercentage.setBackgroundColor(Color.parseColor("#E8F5E9"));
        } else {
            holder.tvPercentage.setTextColor(Color.parseColor("#C62828")); // Red
            holder.tvPercentage.setBackgroundColor(Color.parseColor("#FFEBEE"));
        }
    }

    @Override
    public int getItemCount() {
        return summaryList.size();
    }

    static class SummaryViewHolder extends RecyclerView.ViewHolder {
        TextView tvSubjectName, tvSubjectCode, tvClassesRatio, tvPercentage;

        public SummaryViewHolder(@NonNull View itemView) {
            super(itemView);
            tvSubjectName = itemView.findViewById(R.id.tvSubjectName);
            tvSubjectCode = itemView.findViewById(R.id.tvSubjectCode);
            tvClassesRatio = itemView.findViewById(R.id.tvClassesRatio);
            tvPercentage = itemView.findViewById(R.id.tvPercentage);
        }
    }
}
