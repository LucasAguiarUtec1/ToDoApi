import React, { useEffect } from 'react';
import { createPortal } from 'react-dom';

interface ModalProps {
    isOpen: boolean,
    onClose: () => void,
    title?: string,
    children: React.ReactNode
}

export const Modal:
    React.FC<ModalProps> = ({ isOpen, onClose, title, children }) => {
        useEffect(() => {
            const handleEsc = (e: globalThis.KeyboardEvent) => {
                if (e.key === 'Escape') onClose();
            };
            if (isOpen) {
                document.addEventListener('keydown', handleEsc);
                document.body.style.overflow = 'hidden';
            }
            return () => {
                document.removeEventListener('keydown', handleEsc);
                document.body.style.overflow = 'unset';
            };
        }, [isOpen, onClose]);

        if (!isOpen) return null;

        const modalContent = (
            <div
                className='fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm transition-opacity'
                onClick={onClose}
            >
                <div
                    className='relative w-full max-w-md bg-white rounded-xl shadow-2xl transform transition-all p-6 dark:bg-gray-800'
                    onClick={(e) => e.stopPropagation()}
                    role="dialog"
                    aria-modal="true"
                >
                    <button
                        onClick={onClose}
                        className="absolute top-4 right-4 text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 transition-colors"
                        aria-label="Cerrar modal"
                    >
                        <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>

                    {title && (
                        <h2 className="text-xl font-bold mb-4 text-gray-900 dark:text-white">
                            {title}
                        </h2>
                    )}

                    <div className="mt-2 text-gray-600 dark:text-gray-300">
                        {children}
                    </div>
                </div>
            </div>
        );

        return createPortal(modalContent, document.body);
    }