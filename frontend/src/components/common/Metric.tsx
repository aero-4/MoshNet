type MetricProps = {
    label: string;
    value: number;
};

export function Metric({label, value, color="bg-slate-50"}: MetricProps) {
    return (
        <div className={`${color} rounded-md bg-slate-50 px-3 py-3`} >
            <div className="text-xs font-medium uppercase text-slate-100">{label}</div>
            <div className="mt-1 text-2xl font-semibold text-slate-200">{value}</div>
        </div>
    );
}
