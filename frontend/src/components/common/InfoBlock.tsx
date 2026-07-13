

export function InfoBlock({label, value}) {


    return (
        <div className="rounded-xl p-5 bg-gray-100 flex flex-col gap-3">
            <h1>{label}</h1>
            <p className="text-[14px] text-gray-600">{value}</p>
        </div>
    )

}