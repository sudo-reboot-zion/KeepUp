import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface UIState {
    isSidebarOpen: boolean;
    isNavbarVisible: boolean;
    theme: 'dark' | 'light';
    activeModal: string | null;
}

const initialState: UIState = {
    isSidebarOpen: false,
    isNavbarVisible: true,
    theme: 'light',
    activeModal: null,
};

const uiSlice = createSlice({
    name: 'ui',
    initialState,
    reducers: {
        toggleSidebar: (state) => {
            state.isSidebarOpen = !state.isSidebarOpen;
        },
        setNavbarVisibility: (state, action: PayloadAction<boolean>) => {
            state.isNavbarVisible = action.payload;
        },
        setTheme: (state, action: PayloadAction<'dark' | 'light'>) => {
            state.theme = action.payload;
        },
        setActiveModal: (state, action: PayloadAction<string | null>) => {
            state.activeModal = action.payload;
        },
    },
});

export const { toggleSidebar, setNavbarVisibility, setTheme, setActiveModal } = uiSlice.actions;
export default uiSlice.reducer;
