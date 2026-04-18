import { useEffect } from "react"
import { useAppStore } from "../store/AppStore"
import { Trash2, Check, Pencil, Plus } from "lucide-react"
import { getTasks } from "../api/task"

export default function TasksPage() {
    const { dispatch, state } = useAppStore()

    useEffect(() => {
        const fetchTasks = async () => {
            if (!state.token || !state.user) return;
            try {
                const res = await getTasks(state.user.id, state.token);
                dispatch({
                    type: 'SET_TASKS',
                    payload: res.tasks
                });
            } catch (error) {
                console.error("Error fetching tasks:", error);
            }
        };
        fetchTasks();
    }, [state.token, state.user, dispatch]);

    return (
        <main className="flex items-center min-h-screen bg-slate-950 px-4">
            <section className="mx-auto w-full max-w-3xl rounded-xl border border-slate-800 bg-neutral-800 p-6 shadow-lg">
                <div className="flex items-center justify-between">
                    <h1 className="text-center text-2xl font-bold text-slate-100 py-1 mb-2">
                        Mis Tareas
                    </h1>
                    <button className="bg-cyan-500 text-slate-100 px-2 py-2 rounded-md hover:bg-cyan-400 transition "><Plus size={16} /></button>
                </div>
                <table className="w-full text-sm text-left text-gray-300">
                    <thead className="text-xs uppercase bg-slate-800 text-gray-400">
                        <tr>
                            <th className="px-4 py-3">Tarea</th>
                            <th className="px-4 py-3">Estado</th>
                            <th className="px-4 py-3">Expiracion</th>
                            <th className="px-4 py-3">Acciones</th>
                        </tr>
                    </thead>
                    <tbody>
                        {state.tasks.map((task, index) => (
                            <tr key={task.id} className={`border-t border-slate-700 ${index % 2 === 0 ? "bg-slate-900" : ""} hover:bg-slate-800 cursor-pointer transition-colors`}>
                                <td className="px-4 py-3 font-medium text-gray-200">{task.name}</td>
                                <td className="px-4 py-3">
                                    <span className={`px-2 py-1 rounded-md text-xs font-semibold ${task.completed ? "bg-green-500/10 text-green-400" : task.expired ? "bg-red-500/10 text-red-400" : "bg-yellow-500/10 text-yellow-400"}`}>
                                        {task.completed ? "Completada" : task.expired ? "Expirada" : "Pendiente"}
                                    </span>
                                </td>
                                <td className="px-4 py-3">
                                    {new Date(task.expires_in).toLocaleDateString()}
                                </td>
                                <td className="px-4 py-3">
                                    <div className="flex items-center gap-2">
                                        <button
                                            className="p-2 rounded-md bg-green-500/10 text-green-400 hover:bg-green-500/20 transition"
                                            title="Completar"
                                        >
                                            <Check size={16} />
                                        </button>

                                        <button
                                            className="p-2 rounded-md bg-blue-500/10 text-blue-400 hover:bg-blue-500/20 transition"
                                            title="Editar"
                                        >
                                            <Pencil size={16} />
                                        </button>

                                        <button
                                            className="p-2 rounded-md bg-red-500/10 text-red-400 hover:bg-red-500/20 transition"
                                            title="Eliminar"
                                        >
                                            <Trash2 size={16} />
                                        </button>
                                    </div>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </section>
        </main>
    )
}