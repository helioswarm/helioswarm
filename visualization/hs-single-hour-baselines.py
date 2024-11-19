#Kristopher Klein
#Routine for plotting HelioSwarm Representative Trajectories
#Last Updated 2024-11-18


import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
from matplotlib.colors import ListedColormap, BoundaryNorm
from itertools import combinations
from spacepy import pycdf
from datetime import datetime, timedelta

# Constants
EARTH_RADIUS_KM = 6371.0  # Earth's radius in kilometers
R0 = 12  # Subsolar standoff distance in Earth radii
ALPHA = 0.6  # Empirical factor for magnetopause shape

# Colors for the nine spacecraft
colors = [
    "#56B4E9", "#E69F00", "#000000", "#888888",
    "#F0E442", "#D55E00", "#009E73", "#8D00B2", "#CC79A7"
]

#Define the discrete colormap for number of vertices
discrete_colors = [
    "#1f77b4",  # Blue for M=4
    "#ff7f0e",  # Orange for M=5
    "#2ca02c",  # Green for M=6
    "#d62728",  # Red for M=7
    "#9467bd",  # Purple for M=8
    "#8c564b"   # Brown for M=9
]
cmap = ListedColormap(discrete_colors)
norm = BoundaryNorm(boundaries=[3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5], ncolors=len(discrete_colors))


def magnetopause_boundary(theta, R0=R0, alpha=ALPHA):
    """Calculate the magnetopause boundary based on the Formisano (1979) model."""
    return R0 * (2 / (1 + np.cos(theta)))**alpha

def read_cdf_directory(directory):
    """Read and concatenate Position and Epoch data from all CDF files in the specified directory."""
    position_data_list = []
    epoch_data_list = []

    # Sort file names in ascending order
    sorted_files = sorted(
        [file_name for file_name in os.listdir(directory) if file_name.endswith('.cdf')]
    )

    for file_name in sorted_files:
        file_path = os.path.join(directory, file_name)
        with pycdf.CDF(file_path) as cdf:
            position_data_list.append(cdf['Position'][:])
            epoch_data_list.append(cdf['Epoch'][:])
        
    # Concatenate all data
    position_data = np.concatenate(position_data_list, axis=0)
    epoch_data = np.concatenate(epoch_data_list, axis=0)

    first_time = epoch_data[0]
    last_time = epoch_data[-1]

    # Print the first and last times
    print(f"First time: {first_time}")
    print(f"Last time: {last_time}")
    
    return position_data, epoch_data

def find_closest_time_index(epoch_data, target_time):
    """Find the index of the time closest to the specified target time."""
    target_time_dt = datetime.strptime(target_time, '%Y-%m-%d %H:%M:%S')
    time_diffs = [abs((time - target_time_dt).total_seconds()) for time in epoch_data]
    closest_index = np.argmin(time_diffs)
    return closest_index

def plot_positions(position_data, epoch_data, closest_index):
    """Plot (x, y), (x, z), (y, z) HS positions relative to Earth,
    relative positions of the nodes to the hub, and
    vector displacements and polyhedral geometries
    for a single, specified and surrounding day."""
    # Extract a window of 12 hours before and after the closest time
    start_index = max(closest_index - 12, 0)
    end_index = min(closest_index + 12, len(epoch_data) - 1)
    position_data_window = position_data[start_index:end_index + 1]
    epoch_data_window = epoch_data[start_index:end_index + 1]

    # Extract x, y, z components and normalize to Earth's radius
    x_data = position_data_window[:, 0, 0] / EARTH_RADIUS_KM
    y_data = position_data_window[:, 0, 1] / EARTH_RADIUS_KM
    z_data = position_data_window[:, 0, 2] / EARTH_RADIUS_KM

    # Calculate 3D radial distance and angle from the +X axis
    r_3D = np.sqrt(x_data**2 + y_data**2 + z_data**2)
    theta_3D = np.arccos(x_data / r_3D)  # Angle from the Sun-Earth line (x-axis)

    # Calculate magnetopause boundary for each angle in 3D
    magnetopause_boundary_3D = magnetopause_boundary(theta_3D)

    # Determine colors based on whether each point is inside or outside the magnetosphere in 3D
    inside_colors = np.where(r_3D < magnetopause_boundary_3D, 'blue', 'red')

    # Set panels for plot
    fig, ((ax1, ax2, ax3, ax4), (ax5, ax6, ax7, ax8), (ax9, ax10, ax11, ax12)) = plt.subplots(
        3, 4, figsize=(16, 8),
        gridspec_kw={'width_ratios': [1, 1, 1, 1], 'height_ratios': [1, 1, 1], 
                     'wspace' : 0.2,
                     'hspace' : 0.5
                     }
    )

    # hide (currenlty blank) ax8
    ax8.remove()
    

    # Set axis limits to ±65 Earth radii for the position plots
    axis_limit = 65

    # Title with dynamic start and end times
    fig.suptitle(f'HelioSwarm Observatory at {target_time}', fontsize=14)

    # Plot (x, y) positions
    ax1.plot(x_data, y_data, color='grey', linestyle='-', marker='o', markersize=5)
    ax1.plot(x_data[12], y_data[12], marker='o', markersize=8, color=inside_colors[12])
    ax1.set_ylabel('Y (GSE, $R_E$)')
    ax1.set_xlabel('X (GSE, $R_E$)')
    ax1.set_title('(X, Y) Position')
    ax1.set_xlim(-axis_limit, axis_limit)
    ax1.set_ylim(-axis_limit, axis_limit)
    ax1.set_aspect('equal', adjustable='box')
    ax1.plot(0, 0, 'ko', markersize=6)
    ax1.grid(True)

    # Plot magnetopause boundary in the (x, y) plane
    theta = np.linspace(0, 2 * np.pi, 100)
    R = magnetopause_boundary(theta)
    ax1.plot(R * np.cos(theta), R * np.sin(theta), 'k--', label='Magnetopause Boundary')

    # Plot (x, z) positions
    ax2.plot(x_data, z_data, color='grey', linestyle='-', marker='o', markersize=5)
    ax2.plot(x_data[12], z_data[12], marker='o', markersize=8, color=inside_colors[12])
    ax2.set_ylabel('Z (GSE, $R_E$)')
    ax2.set_xlabel('X (GSE, $R_E$)')
    ax2.set_title('(X, Z) Position')
    ax2.set_xlim(-axis_limit, axis_limit)
    ax2.set_ylim(-axis_limit, axis_limit)
    ax2.set_aspect('equal', adjustable='box')
    ax2.plot(0, 0, 'ko', markersize=6)
    ax2.grid(True)

    # Plot magnetopause boundary in the (x, z) plane
    ax2.plot(R * np.cos(theta), R * np.sin(theta), 'k--', label='Magnetopause Boundary')

    # Plot (y, z) positions
    ax3.plot(y_data, z_data, color='grey', linestyle='-', marker='o', markersize=5)
    ax3.plot(y_data[12], z_data[12], marker='o', markersize=8, color=inside_colors[12])
    ax3.set_xlabel('Y (GSE, $R_E$)')
    ax3.set_ylabel('Z (GSE, $R_E$)')
    ax3.set_title('(Y, Z) Position')
    ax3.set_xlim(-axis_limit, axis_limit)
    ax3.set_ylim(-axis_limit, axis_limit)
    ax3.set_aspect('equal', adjustable='box')
    ax3.plot(0, 0, 'ko', markersize=6)
    ax3.grid(True)

    # Calculate the radius of the magnetopause circle in the (y, z) plane at x = 0
    R_yz = R0 * 2**ALPHA
    
    # Plot the magnetopause circle in the (y, z) plane
    circle_yz = plt.Circle((0, 0), R_yz, color='k', linestyle='--', fill=False, label='Magnetopause Boundary')
    ax3.add_patch(circle_yz)

    # Relative distance plot
    time_axis = [datetime.fromtimestamp(epoch.timestamp()) for epoch in epoch_data_window]  # Convert to datetime objects
    for i in range(1, 9):
        relative_dist = np.linalg.norm(position_data_window[:, i, :] - position_data_window[:, 0, :], axis=1)
        ax4.plot(time_axis, relative_dist, color=colors[i], label=f'Node {i}')

        # Compute and plot the selected hour's relative distance
        relative_dist_center = np.linalg.norm(position_data_window[12, i, :] - position_data_window[12, 0, :])
        ax4.plot(time_axis[12], relative_dist_center, marker='o', color=colors[i])  # Plot the dot at the selected hour

    ax4.set_title("Relative Distance to Hub")
    ax4.set_ylabel("Distance (km)")
    ax4.set_yscale('log')  # Set x-axis to log scale
    ax4.legend(loc='upper right')
    ax4.grid(True)

    # Rotate the x-axis labels for better readability
    for label in ax4.get_xticklabels():
        label.set_rotation(45)
        label.set_horizontalalignment('right')

    # Add hub to node displacements in (x, y) to ax5, (x,z) to ax6, (y,z) to ax7
    for i in range(0, 9):  # Loop through spacecraft 0–8
        delta_x = position_data_window[:, i, 0] - position_data_window[:, 0, 0]  # Difference in x
        delta_y = position_data_window[:, i, 1] - position_data_window[:, 0, 1]  # Difference in y
        delta_z = position_data_window[:, i, 2] - position_data_window[:, 0, 2]  # Difference in z
    
        # Plot the trajectory of separations
        ax5.plot(delta_x, delta_y, label=None, color=colors[i])
        # Highlight the central point
        ax5.plot(delta_x[12], delta_y[12], marker='o', color=colors[i], label=None)

        # Plot the trajectory of separations
        ax6.plot(delta_x, delta_z, label=None, color=colors[i])
        # Highlight the central point
        ax6.plot(delta_x[12], delta_z[12], marker='o', color=colors[i], label=None)

        # Plot the trajectory of separations
        ax7.plot(delta_y, delta_z, label=None, color=colors[i])
        # Highlight the central point
        ax7.plot(delta_y[12], delta_z[12], marker='o', color=colors[i], label=None)

    #Maximum hub to node separation
    delta_limit=1500
        
    # Add labels, title, and grid
    ax5.set_xlabel('$\Delta X$ (km)')
    ax5.set_ylabel('$\Delta Y$ (km)')
    ax5.set_title('Hub-Node Displacement (X, Y)')
    ax5.set_xlim(-delta_limit, delta_limit)
    ax5.set_ylim(-delta_limit, delta_limit)
    ax5.set_aspect('equal', adjustable='box')
    ax5.grid(True)

    # Add labels, title, and grid
    ax6.set_xlabel('$\Delta X$ (km)')
    ax6.set_ylabel('$\Delta Z$ (km)')
    ax6.set_title('Hub-Node Displacement (X, Z)')
    ax6.set_xlim(-delta_limit, delta_limit)
    ax6.set_ylim(-delta_limit, delta_limit)
    ax6.set_aspect('equal', adjustable='box')
    ax6.grid(True)

    # Add labels, title, and grid
    ax7.set_xlabel('$\Delta Y$ (km)')
    ax7.set_ylabel('$\Delta Z$ (km)')
    ax7.set_title('Hub-Node Displacement (Y, Z)')
    ax7.set_xlim(-delta_limit, delta_limit)
    ax7.set_ylim(-delta_limit, delta_limit)
    ax7.set_aspect('equal', adjustable='box')
    ax7.grid(True)

    #calculate all n(n-1) displacements
    # Assuming position_data_window contains the positions at the selected hour
    selected_hour_index = 12  # Index of the hour to analyze
    selected_positions = position_data_window[selected_hour_index, :, :]  # Shape: (9, 3)
    
    # Loop over all pairs of spacecraft
    for i in range(9):  # Loop over the first spacecraft (0 through 8)
        for j in range(i + 1, 9):  # Loop over the second spacecraft (i+1 through 8)
            # Calculate the vector difference between spacecraft i and j
            separation = selected_positions[j, :] - selected_positions[i, :]
            delta_x, delta_y, delta_z = np.abs(separation[0]), np.abs(separation[1]), np.abs(separation[2])
            
            # Plot the (x, y), (x,z) and (y,z) components of the separation
            ax9.plot(delta_x, delta_y, markersize=3, marker='o', color='black', label=None)
            ax10.plot(delta_x, delta_z, markersize=3, marker='o', color='black', label=None)
            ax11.plot(delta_y, delta_z, markersize=3, marker='o', color='black', label=None)
            
    #range for inter spacecraft displacements
    disp_min=10
    disp_max=5000

    #threshold values for kinetic and MHD transitions
    ion_line=100
    MHD_line=1200
    
    ax9.set_xlabel('$\Delta X$ (km)')
    ax9.set_ylabel('$\Delta Y$ (km)')
    ax9.set_xlim(disp_min,disp_max)
    ax9.set_ylim(disp_min,disp_max)
    ax9.set_xscale('log')  # Set x-axis to log scale
    ax9.set_yscale('log')  # Set y-axis to log scale
    ax9.axhline(ion_line, color='k', linestyle='--', linewidth=0.5)
    ax9.axvline(ion_line, color='k', linestyle='--', linewidth=0.5)
    ax9.axhline(MHD_line, color='k', linestyle='--', linewidth=0.5)
    ax9.axvline(MHD_line, color='k', linestyle='--', linewidth=0.5)
    ax9.set_aspect('equal', adjustable='box')
    ax9.set_title('Pairwise Displacements (X, Y)')

    ax10.set_xlabel('$\Delta X$ (km)')
    ax10.set_ylabel('$\Delta Z$ (km)')
    ax10.set_xlim(disp_min,disp_max)
    ax10.set_ylim(disp_min,disp_max)
    ax10.set_xscale('log')  # Set x-axis to log scale
    ax10.set_yscale('log')  # Set y-axis to log scale
    ax10.axhline(ion_line, color='k', linestyle='--', linewidth=0.5)
    ax10.axvline(ion_line, color='k', linestyle='--', linewidth=0.5)
    ax10.axhline(MHD_line, color='k', linestyle='--', linewidth=0.5)
    ax10.axvline(MHD_line, color='k', linestyle='--', linewidth=0.5)
    ax10.set_aspect('equal', adjustable='box')
    ax10.set_title('Pairwise Displacements (X, Z)')

    ax11.set_xlabel('$\Delta Y$ (km)')
    ax11.set_ylabel('$\Delta Z$ (km)')
    ax11.set_xlim(disp_min,disp_max)
    ax11.set_ylim(disp_min,disp_max)
    ax11.set_xscale('log')  # Set x-axis to log scale
    ax11.set_yscale('log')  # Set y-axis to log scale
    ax11.axhline(ion_line, color='k', linestyle='--', linewidth=0.5)
    ax11.axvline(ion_line, color='k', linestyle='--', linewidth=0.5)
    ax11.axhline(MHD_line, color='k', linestyle='--', linewidth=0.5)
    ax11.axvline(MHD_line, color='k', linestyle='--', linewidth=0.5)
    ax11.set_aspect('equal', adjustable='box')
    ax11.set_title('Pairwise Displacements (Y, Z)')

    # Extract positions for the selected hour (index 12)
    points = position_data_window[12, :, :]  # Shape: (9, 3), positions of 9 spacecraft in 3D

    # Generate all polyhedra with 4 or more vertices from the 9 spacecraft positions
    polyhedra = [
        list(comb) for M in range(4, len(points) + 1) for comb in combinations(range(len(points)), M)
    ]

    results = []
    for poly in polyhedra:
        vertices = points[poly]  # Get the positions of the selected spacecraft
        barycenter = np.mean(vertices, axis=0)  # Calculate the barycenter
        centered_vertices = vertices - barycenter # Center the polyhedron at the origin
        T = np.mean([np.outer(v, v) for v in centered_vertices], axis=0)  # Volumetric tensor
        eigenvalues = np.linalg.eigvalsh(T)
        eigenvalues = np.sort(eigenvalues)[::-1]  # Sort eigenvalues in descending order
        a = np.sqrt(eigenvalues[0])  # Largest eigenvalue (size in the largest dimension)
        b = np.sqrt(eigenvalues[1])  # Second-largest eigenvalue
        c = np.sqrt(eigenvalues[2])  # Smallest eigenvalue
        
        # Calculate characteristic size, elongation, and planarity using your definitions
        L = 2 * a  # Characteristic size
        E = 1 - (b / a)  # Elongation
        P = 1 - (c / b)  # Planarity

        # Append results with the number of vertices (len(poly))
        results.append((L, E, P, len(poly)))

    # Extract data from results
    L_values = [r[0] for r in results]  # Characteristic size (L)
    elongation_planarity = [np.sqrt(r[1]**2 + r[2]**2) for r in results]  # sqrt(E^2 + P^2)
    num_vertices = [r[3] for r in results]  # Number of vertices (M)
        
    # Add the scatter plot to ax12
    scatter = ax12.scatter(
        elongation_planarity,
        L_values, 
        c=num_vertices, 
        cmap=cmap, 
        s=50, 
        alpha=0.8
    )

    # Add a colorbar for the discrete colormap
    cbar = plt.colorbar(scatter, ax=ax12, orientation='vertical', ticks=[4, 5, 6, 7, 8, 9])
    cbar.set_label('Number of Vertices (M)', rotation=270, labelpad=15)

    # Set labels and title for ax12
    ax12.set_xlim(0, 1.4)
    ax12.set_ylim(50, 5000)
    ax12.set_yscale('log')  # Set x-axis to log scale
    ax12.set_xlabel('Characteristic Size (L)')
    ax12.set_ylabel('$\sqrt{E^2 + P^2}$')
    ax12.grid(True)
    ax12.set_title('Polyhedral Geometries')
    
    plt.tight_layout()
    plt.show()

def main(directory, target_time):
    """Main function to load data, find the closest time, and plot positions."""
    # Read and concatenate CDF data from directory
    position_data, epoch_data = read_cdf_directory(directory)
    
    # Find the index of the closest time
    closest_index = find_closest_time_index(epoch_data, target_time)
    
    # Plot the filtered data with a 12-hour window around the closest time
    plot_positions(position_data, epoch_data, closest_index)

# Usage example
directory = '../HS-RT/PhB_SRD5B_0x75b/'  # Specify the directory containing CDF files
target_time = '2029-08-07 06:00:00'  # Target time to find the closest hour
main(directory, target_time)
